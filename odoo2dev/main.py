#!/usr/bin/env python

import logging
import click
import click_odoo
from click_odoo import odoo

logger = logging.getLogger(__name__)


def inactive_cron(env):
    # TODO make sure than ir_cron exists
    env.cr.execute("UPDATE ir_cron SET active = 'f'")
    logger.info("ERP crons inactivated")


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
    inactive_cron(env)


if __name__ == "__main__":  # pragma: no cover
    main()
