#!/usr/bin/env python

import base64
import click
import click_odoo
from click_odoo import odoo
from click_odoo_contrib.uninstall import uninstall
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
        uninstall(env, _get_module_names(modules_to_uninstall))
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


def favicon(env):
    path = os.environ.get("ODEV_LOGO_PATH") or "/templates/"
    file = "%s.png" % odoo.tools.config.get("running_env")
    logo = os.path.join(path, file)
    if os.path.isfile(logo):
        with open(logo, 'rb') as file:
            _install_modules(env, "web_favicon")
            print("STATUT", env["ir.module.module"].search(
                [("name", "=", "web_favicon")], limit=1).state)
            env.cr.commit()
            if "favicon" in env["res.company"]._fields.keys():
                # Still a bug there: I don't know why these fields
                # are unknown at this step
                env["res.company"].search([]).write({
                    "favicon_backend": base64.b64encode(file.read()),
                    "favicon_backend_mimetype": "image/png"})
                click.echo(click.style(
                    "Favicon added to companies", fg="green"))
            else:
                click.echo(click.style(
                    "Unknown field favicon_backend: unable to write", fg="red"))


def _get_module_names(modules):
    return [m.strip() for m in modules.split(",")]


def _install_modules(env, modules):
    addons = env["ir.module.module"].search(
        [("name", "in", _get_module_names(modules))])
    addons.button_immediate_install()
    click.echo(click.style("Modules '%s' installed" % modules, fg="green"))


def _check_database(env):
    if not env:
        msg = "Database does not exist"
        raise click.ClickException(msg)


@click.command()
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=False
)
def main(env):
    """ Features:
\n - inactive crons and outgoings mail
\n - install list of modules coming from ``ODEV_INSTALL`` env var (comma separated)
\n - uninstall list of modules coming from ``ODEV_UNINSTALL`` env var (comma separated)
\n - reset users password to ``admin`` when ``ODEV_RESET_PASSWORD`` var is set to True
\n - install ``web_favicon`` to make your instance with a different look and
feel (``ODEV_LOGO_PATH`` env var with file named 'dev.png' inside active this feature)
    """
    _check_database(env)
    click.echo("Operations on database '%s':" % env.cr.dbname)
    inactive_cron(env)
    inactive_mail(env)
    install_uninstall(env)
    reset_password(env)
    favicon(env)
    env.cr.commit()


if __name__ == "__main__":  # pragma: no cover
    main()
