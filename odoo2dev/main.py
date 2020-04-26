#!/usr/bin/env python

import base64
import click
import click_odoo
from click_odoo import odoo
import os
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
        click.echo(click.style(" - Favicon added to companies", fg="green"))
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


@click.command()
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=False
)
def main(env):
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


if __name__ == "__main__":  # pragma: no cover
    main()
