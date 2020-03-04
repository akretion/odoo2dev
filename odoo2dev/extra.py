#!/usr/bin/env python3

import click
import click_odoo
from click_odoo import odoo


@click.command()
@click_odoo.env_options(
    default_log_level="info", with_database=True, with_rollback=False
)
def main(env):
    """ TODO 
		- install web_ribbon if available
		- ...
    """
    
    print("You're there")


if __name__ == "__main__":  # pragma: no cover
    main()
