=====
About
=====

.. BADGES_START
   
.. image:: https://img.shields.io/pypi/v/parser201.svg
      :target: https://pypi.python.org/pypi/parser201

.. image:: https://img.shields.io/github/v/tag/geozeke/parser201.svg
      :target: https://img.shields.io/github/v/tag/geozeke/parser201

.. image:: https://img.shields.io/travis/geozeke/parser201.svg
      :target: https://travis-ci.com/geozeke/parser201

.. image:: https://readthedocs.org/projects/parser201/badge/?version=latest
      :target: https://parser201.readthedocs.io/en/latest/?badge=latest
      :alt: Documentation Status
     
.. image:: https://img.shields.io/pypi/status/parser201.svg
      :target: https://img.shields.io/pypi/status/parser201
      
.. image:: https://img.shields.io/pypi/pyversions/parser201.svg
      :target: https://img.shields.io/pypi/pyversions/parser201

.. image:: https://img.shields.io/github/last-commit/geozeke/parser201.svg
      :target: https://img.shields.io/github/last-commit/geozeke/parser201

.. image:: https://img.shields.io/github/license/geozeke/parser201.svg
      :target: https://img.shields.io/github/license/geozeke/parser201
   
.. BADGES_END

Free software: MIT license

Features
--------

The centerpiece of the parser201 module is the ``LogParser`` class. The class initializer takes a line from an Apache log file and extracts the individual fields into properties within an object.

* Parses entries (lines) from Apache log files into objects with a separate property for each field in the log entry.
* Prints log objects as strings in a presentation format.

Documentation
-------------

https://parser201.readthedocs.io

Development Lead
----------------

Peter Nardi <pete@nardi.com>

Source Code
-----------

Available on github: parser201_.

.. _parser201: https://github.com/geozeke/parser201

Package Framework
-----------------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
