#!/usr/bin/env python

from psycopg2 import ProgrammingError
import click
import click_odoo
from click_odoo import odoo


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


@click.command()
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=False
)
@click.option(
    "--if-exists", is_flag=True, help="Don't report error if database doesn't exist"
)
def main(env, if_exists):
    if not env:
        msg = "Database does not exist"
        if if_exists:
            click.echo(click.style(msg, fg="yellow"))
            return
        else:
            raise click.ClickException(msg)
    click.echo("On database '%s':" % env.cr.dbname)
    inactive_cron(env)
    inactive_mail(env)


if __name__ == "__main__":  # pragma: no cover
    main()
