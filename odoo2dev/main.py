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
        click.echo(click.style("ERP user's password are reset", fg="green"))


def install_uninstall(env):
    # TODO improve according to module state
    modules_to_install = os.environ.get("ODEV_INSTALL")
    modules_to_uninstall = os.environ.get("ODEV_UNINSTALL")
    if modules_to_uninstall:
        _uninstall(env, _get_module_names(modules_to_uninstall))
        click.echo(click.style(
            "Modules '%s' uninstalled" % modules_to_uninstall, fg="green"))
    if modules_to_install:
        _install_modules(env, modules_to_install)


def inactive_cron(env):
    try:
        env.cr.execute("UPDATE ir_cron SET active = 'f'")
        click.echo(click.style("ERP crons inactivated", fg="green"))
    except ProgrammingError as e:
        msg = "Probably no ir_cron table in this database"
        click.echo(click.style(msg, fg="red"))
        raise e
    except Exception as e:
        raise e


def inactive_mail(env):
    try:
        env.cr.execute("UPDATE ir_mail_server SET active = 'f'")
        click.echo(click.style("ERP outgoing mail are inactivated", fg="green"))
    except Exception as e:
        raise e


def set_favicon(env):
    data = _get_favicon_data(env)
    if data:
        env.cr.execute("""
            UPDATE res_company
            SET favicon_backend = %s,
                favicon_backend_mimetype = 'image/png'""", (data,))
        click.echo(click.style(
            "Favicon added to companies", fg="green"))
    else:
        click.echo(click.style("No favicon file", fg="blue"))


def _get_favicon_data(env):
    _install_modules(env, "web_favicon")
    path = os.environ.get("ODEV_LOGO_PATH") or "/templates/"
    file = "%s.png" % odoo.tools.config.get("running_env")
    logo = os.path.join(path, file)
    if os.path.isfile(logo):
        with open(logo, 'rb') as file:
            return base64.b64encode(file.read())


def _get_module_names(modules):
    return [m.strip() for m in modules.split(",")]


def _uninstall(env, module_names):
    addons = env["ir.module.module"].search([("name", "in", module_names)])
    addons.button_immediate_uninstall()
    module_states = {x.name: x.state for x in addons}
    click.echo(click.style(
        "Uninstallation module state '%s'" % module_states, fg="green"))


def _install_modules(env, modules):
    addons = env["ir.module.module"].search(
        [("name", "in", _get_module_names(modules))])
    addons.button_immediate_install()
    module_states = {x.name: x.state for x in addons}
    click.echo(click.style(
        "Installation: modules states '%s'" % module_states, fg="green"))
    env.cr.commit()


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
    click.echo("Operations on database '%s':" % env.cr.dbname)
    inactive_cron(env)
    inactive_mail(env)
    install_uninstall(env)
    reset_password(env)
    set_favicon(env)
    env.cr.commit()


if __name__ == "__main__":  # pragma: no cover
    main()
