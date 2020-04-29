#!/usr/bin/env python

import base64
import click
import click_odoo
from click_odoo import odoo
import os
import subprocess
import runpy
from psycopg2 import ProgrammingError


def reset_password(env):
    reset = os.environ.get("ODEV_RESET_PASSWORD")
    if reset:
        env.cr.execute("UPDATE res_users SET password = 'admin'")
        click.echo(click.style(" - user's password are reset to 'admin'", fg="green"))


def install_uninstall(env):
    modules_to_install = os.environ.get("ODEV_INSTALL")
    modules_to_uninstall = os.environ.get("ODEV_UNINSTALL")
    if modules_to_uninstall:
        _uninstall(env, _get_module_names(modules_to_uninstall))
    if modules_to_install:
        _install_modules(env, modules_to_install)


def inactive_cron(env):
    try:
        env.cr.execute("UPDATE ir_cron SET active = 'f'")
        click.echo(click.style(" - crons are inactivated", fg="green"))
    except ProgrammingError as e:
        msg = "Probably no ir_cron table in this database"
        click.echo(click.style(msg, fg="red"))
        raise e
    except Exception as e:
        raise e


def inactive_mail(env):
    try:
        env.cr.execute("UPDATE ir_mail_server SET active = 'f'")
        click.echo(click.style(" - outgoing mail servers are inactivated", fg="green"))
    except Exception as e:
        raise e


def set_favicon(env):
    res = _install_modules(env, "web_favicon")
    if "web_favicon" not in res:
        return
    data = _get_favicon_data(env)
    if data:
        env.cr.execute(
            """
            UPDATE res_company
            SET favicon_backend = %s,
                favicon_backend_mimetype = 'image/png'""",
            (data,),
        )
        click.echo(click.style(" - favicon added to companies", fg="green"))
    else:
        click.echo(click.style("No favicon file", fg="blue"))


def _get_favicon_data(env):
    path = os.environ.get("ODEV_LOGO_PATH") or "/templates/"
    file = "%s.png" % odoo.tools.config.get("running_env")
    logo = os.path.join(path, file)
    if os.path.isfile(logo):
        with open(logo, "rb") as file:
            return base64.b64encode(file.read())


def _get_module_names(modules):
    return [m.strip() for m in modules.split(",")]


def _uninstall(env, module_names):
    addons = env["ir.module.module"].search([("name", "in", module_names)])
    addons.button_immediate_uninstall()
    uninstalled = [x.name for x in addons if x.state == "uninstalled"]
    if uninstalled:
        click.echo(
            click.style(
                " - successfull modules uninstallation %s" % uninstalled, fg="green"
            )
        )
    _check_module_state(module_names, uninstalled, operation="uninstall")
    env.cr.commit()
    return uninstalled


def _install_modules(env, modules):
    modules_list = _get_module_names(modules)
    addons = env["ir.module.module"].search([("name", "in", modules_list)])
    addons.button_immediate_install()
    installed = [x.name for x in addons if x.state == "installed"]
    if installed:
        click.echo(
            click.style(
                " - successfull modules installation %s" % installed, fg="green"
            )
        )
    _check_module_state(modules_list, installed)
    env.cr.commit()
    return installed


def _check_module_state(modules_todo, modules_operated, operation="install"):
    diff = set(modules_todo) - set(modules_operated)
    if diff:
        click.echo(
            click.style(
                "Failed to '%s' these modules %s: check your addons path"
                % (operation, list(diff)),
                fg="yellow",
            )
        )


def _check_database(env):
    if not env:
        msg = "Database does not exist"
        raise click.ClickException(msg)


def execute_external_script(env, script, script_args):
    """ Script path executed as last operation
    """
    global_vars = {"env": env}
    # check if it's an anthem script and trigger it
    if script == "anthem":
        if not script_args:
            click.echo(click.style("Missing anthem args to be executed", fg="red"))
            return
        process = subprocess.Popen(
            ["anthem", script_args[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        with process.stdout:
            _log_subprocess_output(process.stdout)
        return
    # or launch as standard python script aka python -m myscript
    click.echo(click.style(" - script '%s' being executed." % script, fg="green",))
    if not os.path.isfile(script):
        raise Exception("Script '%s' is not an accessible file." % script)
    # TODO use script_args ??
    return runpy.run_path(script, init_globals=global_vars, run_name="__main__")


def _log_subprocess_output(pipe):
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        line = line.decode("utf-8").rstrip("\n")
        click.echo(click.style(line, fg="yellow"))


@click.command(
    help="""
odoo2dev package providing facilities to use a dump of your production database
in your dev environment.

The following operations are executed:

Always:

  - deactivate crons and outgoing mails

Optionally and depending on the inputs:

  - execute provided script with [SCRIPT] [SCRIPT_ARGS] as final operation \n
  - install or uninstall a comma-separated list of modules\n
  - reset password to `admin`\n
  - apply favicon on odoo instance

"""
)
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=False
)
@click.argument(
    "script", envvar="ODEV_SCRIPT", required=False,
)
@click.argument("script-args", envvar="ODEV_SCRIPT_ARGS", required=False, nargs=-1)
def main(env, script, script_args):
    """ each function names are self explained
    """
    _check_database(env)
    click.echo("Operations on Odoo database '%s':" % env.cr.dbname)
    inactive_cron(env)
    inactive_mail(env)
    install_uninstall(env)
    reset_password(env)
    set_favicon(env)
    env.cr.commit()
    # Finally execute script if provided
    if script:
        execute_external_script(env, script, script_args)


if __name__ == "__main__":  # pragma: no cover
    main()
