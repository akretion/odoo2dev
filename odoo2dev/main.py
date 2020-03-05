#!/usr/bin/env python

from psycopg2 import ProgrammingError
import os
import click
import click_odoo
from click_odoo import odoo
from click_odoo_contrib.uninstall import uninstall


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
        click.echo(click.style("Modules '%s' uninstalled" % modules_to_uninstall, fg="green"))
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


def _get_module_names(modules):
    return [m.strip() for m in modules.split(",")]


def _install_modules(env, modules):
    addons = env["ir.module.module"].search([("name", "in", _get_module_names(modules))])
    addons.button_immediate_install()
    env.cr.commit()
    click.echo(click.style("Modules '%s' installed" % modules, fg="green"))


def _check_database(env, if_exists):
    if not env:
        msg = "Database does not exist"
        if if_exists:
            click.echo(click.style(msg, fg="yellow"))
            return
        else:
            raise click.ClickException(msg)


@click.command()
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=False
)
@click.option(
    "--if-exists", is_flag=True, help="Don't report error if database doesn't exist"
)
def main(env, if_exists):
    """ Features:
\n - inactive crons and outgoings mail
\n - install list of modules coming from ``ODEV_INSTALL`` env var (comma separated)
\n - uninstall list of modules coming from ``ODEV_UNINSTALL`` env var (comma separated)
\n - reset users password to ``admin`` when ``ODEV_RESET_PASSWORD`` var is set to True
    """
    _check_database(env, if_exists)
    click.echo("Operations on database '%s':" % env.cr.dbname)
    inactive_cron(env)
    inactive_mail(env)
    install_uninstall(env)
    reset_password(env)


if __name__ == "__main__":  # pragma: no cover
    main()
