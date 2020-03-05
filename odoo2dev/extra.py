#!/usr/bin/env python

from psycopg2 import ProgrammingError
import os
import base64
import click
import click_odoo
from click_odoo import odoo
from odoo.tools import config


def favicon(env):
    logo = '/templates/%s.png' % config.get("running_env")
    if os.path.isfile(logo):
        with open(logo, 'rb') as file:
            module = env["ir.module.module"].search(
                [("name", "=", "web_favicon"), ("state", "in", ["to install", "installed"])])
            if module:
                if module.state == "to install":
                    module.button_immediate_install()
                env["res.company"].search([]).write(
                    {'favicon_backend': base64.b64encode(file.read()),
                    'favicon_backend_mimetype': 'image/png'})
        click.echo(click.style("Favicon added to companies", fg="green"))
    else:
        click.echo(click.style("No logo file in /templates according to your environment", fg="yellow"))

@click.command()
@click_odoo.env_options(
    default_log_level="warn", with_database=True, with_rollback=True
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
    favicon(env)


if __name__ == "__main__":  # pragma: no cover
    main()
