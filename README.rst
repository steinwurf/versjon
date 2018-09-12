Introduction
============
.. .. image:: https://ci.appveyor.com/api/projects/status/ INSERT ID /branch/master?svg=true
        :target: https://ci.appveyor.com/project/SteinwurfApS/versjon

.. .. image:: https://travis-ci.org/steinwurf/versjon.svg?branch=master
        :target: https://travis-ci.org/steinwurf/versjon

The versions json generator ``versjon`` is a very small tool for generating a
json file containing the name and url of versions in a folder.

Command-line arguments
----------------------

Whn invoking ``versjon`` there are three mandatory arguments::

    versjon directory url_format output

* ``directory`` specifies the directory containing the versions.
  Each version should have it's own directory in this directory.
* ``url_format`` is a python string which uses the new named format
  placeholders to specify how the the url for each version should look.
  Only the version name is provide as the value 'version'.
  Example:

	 http://127.0.0.1/project/versions/{version}.html

* ``output`` the output json file.
