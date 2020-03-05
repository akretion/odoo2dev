.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :alt: Python support: 3.6
.. image:: https://img.shields.io/badge/python-2.7-blue.svg
    :alt: Python support: 2.7

.. .. image:: https://travis-ci.org/akretion/odoo2dev.svg?branch=master
..     :target: https://travis-ci.org/akretion/odoo2dev
.. .. image:: https://coveralls.io/repos/akretion/odoo2dev/badge.png?branch=master
..     :target: https://coveralls.io/r/akretion/odoo2dev?branch=master

.. image:: https://img.shields.io/badge/Odoo-v8, v10, v12-blueviolet.svg
    :alt: Odoo

========
odoo2dev
========

``odoo2dev`` is a python3/2 package providing facilities to use a dump of your production in your dev environment.


Features
========

Features are triggered by these shell entrypoints:


``odev``
--------

- inactive crons and outgoing mail
- install list of modules coming from ``ODEV_INSTALL`` env var (comma separated)
- uninstall list of modules coming from env var ``ODEV_UNINSTALL`` env var (comma separated)
- reset users password to ``admin`` when ``ODEV_RESET_PASSWORD`` var is set to True


``odev+``
---------

Some extra features here (more to come):

- install ``web_favicon`` to make your instance with a different look and feel:
  set path in ``ODEV_LOGO_PATH`` env var and put a file named 'dev.png' in this place


Install
=======

Install this lib in your project with

``pip install git+https://github.com/akretion/odoo2dev.git#egg=odoo2dev``.


``odoo2dev`` relies on the excellent ``click-odoo-contrib``.
