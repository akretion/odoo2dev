.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :alt: Python support: 3.6
.. image:: https://travis-ci.org/grap/odoo2dev.svg?branch=master
    :target: https://travis-ci.org/grap/odoo2dev
.. image:: https://coveralls.io/repos/grap/odoo2dev/badge.png?branch=master
    :target: https://coveralls.io/r/grap/odoo2dev?branch=master

========
odoo2dev
========

``odoo2dev`` is a python3/2 package providing facilities to use a dump of your production in 
your dev environment.

You may install install this lib in your project with ``pip install git+https://github.com/akretion/odoo2dev.git#egg=odoo2dev``.

Features
--------

2 entry points allowing to:

- ``odev`` to inactive crons and outgoing mail
- ``odev+`` for extra features like install web_favicon to make your instance with a different look and feel and more to come.
