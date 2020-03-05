========
odoo2dev
========


.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :alt: Python support: 3.6
.. image:: https://img.shields.io/badge/python-2.7-blue.svg
    :alt: Python support: 2.7
.. image:: https://img.shields.io/badge/Odoo-v8, v10, v12-blueviolet.svg
    :alt: Odoo


``odoo2dev`` is a python3/2 package providing facilities to use a dump of your production in your dev environment.


Features
========

Features are triggered by these shell entrypoints:


``odev``
--------

.. code::

  Features:

  - inactive crons and outgoings mail

  - install list of modules coming from ``ODEV_INSTALL`` env var (comma
      separated)

  - uninstall list of modules coming from ``ODEV_UNINSTALL`` env var (comma
      separated)

  - reset users password to ``admin`` when ``ODEV_RESET_PASSWORD`` var is
      set to True      

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


``odev+``
---------

.. code::

  Features:

  - install ``web_favicon`` to make your instance with a different look and
  feel:  set path in ``ODEV_LOGO_PATH`` env var and put a file named
  'dev.png' in this place

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
=======

Install this lib in your project with

``pip install git+https://github.com/akretion/odoo2dev.git#egg=odoo2dev``.


``odoo2dev`` relies on the excellent ``click-odoo-contrib``.
