Introduction
============

.. image:: https://img.shields.io/appveyor/ci/SteinwurfApS/versjon/master.svg?style=flat-square&logo=appveyor
    :target: https://ci.appveyor.com/project/SteinwurfApS/versjon

.. image:: https://travis-ci.org/steinwurf/versjon.svg?branch=master
    :target: https://travis-ci.org/steinwurf/versjon

A Sphinx extension and tool for linking muiltiple versions of your project's
documentation (without the need for special services such as readthedocs.org).

Installation
------------

Install the ``versjon`` tool using ``pip``::

    python -m pip install versjon

Register the Sphinx extension in your project's Sphinx configuration stored in
``conf.py``::

    ...
    extensions = ['versjon']
    ...

How it works
------------

1. Make sure you have the ``versjon`` extension installed for all the versions
   of your documentation where you want to use ``versjon``.

First you build your do


Using services like readthedocs.org makes it easy to generate and host different
versions of a project's documentation. However, for static sites  The versions JSON generator ``versjon`` is a very small tool for generating a
JSON file containing the name and url of versions in a folder.
