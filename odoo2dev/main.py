#!/usr/bin/env python

import base64
import click
import click_odoo
from click_odoo import odoo
import os
import subprocess
import runpy
from psycopg2 import ProgrammingError


def reset_password(env, password):
    if password:
        env.cr.execute("UPDATE res_users SET password = 'admin'")
        click.echo(click.style(" - user's passwords are reset to 'admin'", fg="green"))


def install_uninstall(env, install, remove):
    if remove:
        _uninstall(env, _get_module_names(remove))
    if install:
        _install_modules(env, install)


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


def make_outgoing_mails_safe(env):
    try:
        # Inactivation
        env.cr.execute("UPDATE ir_mail_server SET active = 'f'")
        # Add fake mail server settings, you've to install matching server yourself
        env.cr.execute(
            """
        INSERT INTO ir_mail_server (
        name, smtp_host, smtp_port, smtp_encryption, active, sequence)
        VALUES (
        'Here settings to catch your mails: install mailcatcher or mailhog to use it',
        'smtp://127.0.0.1', 1025, 'none', 't', 1)
            """
        )
        click.echo(
            click.style(
                " - outgoing mail servers are inactivated (except a fake one for test)",
                fg="green",
            )
        )
    except Exception as e:
        raise e


def set_favicon(env, favicon):
    res = _install_modules(env, "web_favicon")
    if "web_favicon" not in res:
        return
    data = _get_favicon_data(favicon)
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


def _get_favicon_data(favicon):
    path = favicon or "/templates/"
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


def execute_anthem_script(script, script_args):
    if script == "anthem" and script_args:
        cmd, cmd_args = script, script_args[0]
    elif script[:6] == "anthem" and " " in script:
        cmd, cmd_args = script[:6], script[6:].strip()
    else:
        click.echo(
            click.style(
                "Impossible to execute script with these arguments: "
                "script '%s' args '%s'" % (script, script_args),
                fg="red",
            ),
        )
        return
    process = subprocess.Popen(
        [cmd, cmd_args.strip()], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    with process.stdout:
        _log_subprocess_output(process.stdout)
    click.echo(
        click.style("'%s %s' script is executed: " % (cmd, cmd_args), fg="green"),
    )
    return


def execute_external_script(env, script, script_args):
    """ Script path executed as last operation
    """
    global_vars = {"env": env}
    # check if it's an anthem script and trigger it
    if script[:6] == "anthem":
        return execute_anthem_script(script, script_args)
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


def log_deprecated():
    " Some env var have been renamed "
    map_ = {
        "ODEV_RESET_PASSWORD": "ODEV_PASSWORD_RESET",
        "ODEV_UNINSTALL": "ODEV_REMOVE",
        "ODEV_LOGO_PATH": "ODEV_FAVICON_PATH",
    }
    for old, new in map_.items():
        if os.environ.get(old):
            msg = "Env var %s have been replaced by %s. " % (old, new)
            msg += "Please update this var in your environment"
            click.echo(click.style(msg, fg="red"))


@click.command(
    help="""
odoo2dev package providing facilities to use a dump of your production database
in your dev environment.

The following operations are executed:

Always:

  - deactivate crons and outgoing mails

Optionally and depending on the inputs:

  - install or uninstall a comma-separated list of modules\n
  - reset password to `admin`\n
  - apply favicon on odoo instance
  - execute provided script with [SCRIPT] [SCRIPT_ARGS] as final operation \n

"""
)
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=False
)
@click.argument("script", envvar="ODEV_SCRIPT", required=False)
@click.argument("script-args", required=False, nargs=-1)
@click.option(
    "--favicon",
    "-f",
    envvar="ODEV_FAVICON_PATH",
    required=False,
    help="Apply a favicon to your Odoo instance. Require to make "
    "available `web_favicon` module. "
    "This is the same behavior that using ODEV_FAVICON_PATH env var",
)
@click.option(
    "--install",
    "-i",
    envvar="ODEV_INSTALL",
    required=False,
    help="A comma-separated list of modules to install. "
    "This is the same behavior that using ODEV_INSTALL env var",
)
@click.option(
    "--remove",
    "-r",
    envvar="ODEV_REMOVE",
    required=False,
    help="A comma-separated list of modules to uninstall. "
    "This is the same behavior that using ODEV_REMOVE env var",
)
@click.option(
    "--password",
    "-p",
    envvar="ODEV_PASSWORD_RESET",
    required=False,
    help="Reset password to `admin`. "
    "This is the same behavior that using ODEV_PASSWORD_RESET env var",
)
def main(env, script, script_args, favicon, install, remove, password):
    """ each function names are self explained
    """
    log_deprecated()
    _check_database(env)
    click.echo("Operations on Odoo database '%s':" % env.cr.dbname)
    inactive_cron(env)
    make_outgoing_mails_safe(env)
    install_uninstall(env, install, remove)
    reset_password(env, password)
    set_favicon(env, favicon)
    env.cr.commit()
    # Finally execute script if provided
    if script:
        execute_external_script(env, script, script_args)


if __name__ == "__main__":  # pragma: no cover
    main()
