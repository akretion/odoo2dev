odoo2dev
========

.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

.. image:: https://img.shields.io/badge/python-2.7 | 3.5+-blue.svg
    :alt: Python support

.. image:: https://img.shields.io/badge/Odoo-8.0  |  10.0  |  12.0-blueviolet.svg
    :alt: Odoo


**odoo2dev** is a python3/2 package providing facilities to use a dump of your production database in your dev environment.
It builds on top of `click-odoo <https://github.com/acsone/click-odoo>`__.

The motivations for this library is to handle redundant operations in a simple and convenient way.

Features
--------

The following operations are executed:

Always:
  - deactivate crons and outgoing mails

Other operations are optionnal and depends of options or environment vars:

Optionally and depending on the inputs:
  - ODEV_INSTALL: comma-separated list of modules to install
  - ODEV_UNINSTALL: comma-separated list of modules to uninstall
  - ODEV_RESET_PASSWORD: boolean flag to reset password to default 'admin'
  - ODEV_LOGO_PATH: path to the logo (favicon) that should be used
  - execute provided script with [SCRIPT] [SCRIPT_ARGS] or ODEV_SCRIPT env vars


Install
-------

Install this lib in your project with

``pip install git+https://github.com/akretion/odoo2dev.git@master#egg=odoo2dev``


**odoo2dev** relies on the excellent
`click-odoo <https://github.com/acsone/click-odoo>`__


Usage
-----

- You may define a script to executed as last step

.. code-block:: bash

  pg_restore -d my_db my.dump ; odev my-script -d my_db ; odoo


Recurrent inputs can be preferably be used with environment variables like below


- Set environment variables, for example on your docker-compose file, with key-value pairs:

.. code-block:: yaml

  - ODEV_SCRIPT=/odoo/my-script
  # in combination with https://github.com/camptocamp/anthem
  - ODEV_SCRIPT=anthem songs.my-script::main
  - ODEV_INSTALL=web_environment_ribbon,my_other_module
  - ODEV_UNINSTALL=module_for_prod_only,my_useless_module
  - ODEV_RESET_PASSWORD=True
  - ODEV_LOGO_PATH=/my_own_path

- Execute odoo2dev through **odev** command when needed, typically after database restore, i.e.:

.. code-block:: bash

  pg_restore -d my_db my.dump ; odev -d my_db ; odoo


Here is a result example

.. figure:: /docs/output_example.png
    :alt: output example


Command-line options:
  -c, --config FILE    Specify the Odoo configuration file. Other ways to
                       provide it are with the ODOO_RC or OPENERP_SERVER
                       environment variables, or ~/.odoorc (Odoo >= 10) or
                       ~/.openerp_serverrc.
  -d, --database TEXT  Specify the database name. If present, this parameter
                       takes precedence over the database provided in the Odoo
                       configuration file.
  --log-level TEXT     Specify the logging level. Accepted values depend on
                       the Odoo version, and include debug, info, warn, error.
                       [default: warn]
  --logfile FILE       Specify the log file.
  --help               Show this message and exit.


Roadmap / Limitations
---------------------

- odoo2dev doesn't ensure than modules to install or uninstall are available on addons path before launch the command.
- if required base tables are not available in called database (``ir_mail_server``, ``res_users``, etc) errors can be triggered (example with a not odoo db).
- other versions than even ones could works but not tested until now


Credits
-------

Author:

- David BEAL (`Akretion <https://www.akretion.com>`__)


Contributors:

- Kevin Khao (`Akretion <https://www.akretion.com>`__)
- Welcome


Maintainer
----------

`Akretion <https://www.akretion.com>`__
