# -*- coding: utf-8 -*-
"""Installer for the cpskin.caching package."""

from setuptools import find_packages, setup

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
    name="cpskin.caching",
    version="1.1.3",
    description="Caching configuration for cpskin",
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
    author="Jean-Francois Roche",
    author_email="jfroche@affinitic.be",
    url="https://pypi.python.org/pypi/cpskin.caching",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["cpskin"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api",
        "setuptools",
        "z3c.jbot",
        "Products.MemcachedManager",
        "z3c.unconfigure",
        "collective.monkeypatcher>=1.0.1",
        "python-memcached",
        "cpskin.minisite",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
