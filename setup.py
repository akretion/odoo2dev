# Copyright (C) 2020 - Today: Akretion (http://www.akretion.com)
# @author: David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from setuptools import find_packages
import setuptools


setuptools.setup(
    name="odoo2dev",
    version="0.3.2",
    author="Akretion",
    author_email="contact@akretion.com",
    license="AGPLv3+",
    description="Make your production odoo db copy, dev ready",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/akretion/odoo2dev",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Odoo",
        "Topic :: Software Development :: Dev tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Environment :: Console",
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points=dict(console_scripts=[
        "odev=odoo2dev.main:main",
    ]),
    keywords=[
        "Odoo", "Development", "ERP", "Module", "Security"
    ],
)
