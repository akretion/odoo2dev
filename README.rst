odoo2dev
========

.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :alt: Python support: 3.6

.. image:: https://img.shields.io/badge/python-2.7-blue.svg
    :alt: Python support: 2.7

.. image:: https://img.shields.io/badge/Odoo-8.0 | 10.0 | 12.0-blueviolet.svg
    :alt: Odoo


**odoo2dev** is a python3/2 package providing facilities to use a dump of your production in your dev environment.


Features
--------

Features are triggered by this shell entrypoint: **odev**

- inactive crons and outgoings mail
- install list of modules if provided with server env var.
- uninstall list of modules if provided with server env var.
- reset users password to ``admin`` when **ODEV_RESET_PASSWORD** var is set to True.
- install **web_favicon** to make your instance with a different look and feel (**ODEV_LOGO_PATH** env var with file named ``dev.png`` inside active this feature)

Options:
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


Install
-------

Install this lib in your project with

``pip install git+https://github.com/akretion/odoo2dev.git@master#egg=odoo2dev``.


**odoo2dev** relies on the excellent
`click-odoo <https://github.com/acsone/click-odoo>`__


Usage
-----

- fill you server environment or your docker-compose file with the choosen keys:

.. code-block:: yaml

  - ODEV_INSTALL=web_environment_ribbon,my_other_module
  - ODEV_UNINSTALL=module_for_prod_only,my_useless_module
  - ODEV_RESET_PASSWORD=True
  - ODEV_LOGO_PATH=/my_own_path

- when you restore you database, add **odev** cmd, i.e.:

.. code-block:: bash

  pg_restore -d my_db my.dump ; odev -d my_db ; odoo


Roadmap / Limitations
---------------------

- odoo2dev doesn't ensure than modules to install or uninstall are available on addons path before launch the command.
- if required base tables are not available in called database (``ir_mail_server``, ``res_users``, etc) errors can be triggered (example with a not odoo db).
- for any project you need to execute specific script to complete **odev** work, then support for additional script will be added at the end of the execution.
- other versions than even ones could works but not tested until now


Credits
-------

Author:

- David BEAL (`Akretion <https://www.akretion.com>`__)


Contributors:

- Welcome


Maintainer
----------

`Akretion <https://www.akretion.com>`__
