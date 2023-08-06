# -*- coding: utf-8 -*-
"""Installer for the cpskin.citizen package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read()
    + "\n"
    + "Contributors\n"
    + "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="cpskin.citizen",
    version="1.4.1",
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Martin Peeters",
    author_email="martin.peeters@affinitic.be",
    url="https://pypi.python.org/pypi/cpskin.citizen",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["cpskin"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "borg.localrole",
        "collective.geo.leaflet",
        "collective.monkeypatcher",
        "collective.z3cform.select2",
        "imio.dashboard",
        "plone.api",
        "plone.app.contenttypes",
        "plone.app.dexterity",
        "plone.app.iterate",
        "plone.app.stagingbehavior",
        "plone.principalsource",
        "setuptools",
        "z3c.jbot",
        "geocoder",
    ],
    extras_require={
        "test": [
            "collective.contact.core",
            "plone.app.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
            "Mock",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
