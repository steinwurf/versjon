Introduction
============

.. image:: https://img.shields.io/appveyor/ci/SteinwurfApS/versjon/master.svg?style=flat-square&logo=appveyor
    :target: https://ci.appveyor.com/project/SteinwurfApS/versjon

.. image:: https://travis-ci.org/steinwurf/versjon.svg?branch=master
    :target: https://travis-ci.org/steinwurf/versjon

A Sphinx extension and tool for linking muiltiple versions of your project's
documentation (without the need for special services such as readthedocs.org).

Useful if you build and host your documentation as a static site.

Installation
------------

1. Install the ``versjon`` tool using ``pip``::

      python -m pip install versjon

2. Register the Sphinx extension in your project's Sphinx configuration stored in
   ``conf.py``::

       ...
       extensions = ['versjon']
       ...

3. Add the ``versjon.html`` template to the HTML sidebar, this is done by
   adding/modifying the ``html_sidebars`` option in Sphinx's ``conf.py``.

   Exampel::

       html_sidebars = {'**': ['globaltoc.html', 'searchbox.html', 'versjon.html']}

   If you want to customize how the versions are presented in HTML e.g. adapt
   them to your theme see the customization section.


Building the docs
-----------------

1. Make sure you have the ``versjon`` extension installed
   (in Sphinx's ``conf.py``)for all the versions of your documentation where you
   want to use ``versjon``.

2. Build all the different versions of your documentation into a common
   directory. For example generating all the docs in the ``site`` directory::

       git checkout 2.0.0
       sphinx-build... -D version=2.0.0 ... site/build_2.0.0

       ...

       git checkout 5.1.1
       sphinx-build... -D version=5.1.1 ... site/build_5.1.1


   ``versjon`` will use whatever ``version`` is specified in the Sphinx
   configuration: https://www.sphinx-doc.org/en/master/usage/configuration.html
   If you have the specified the ``version`` number in ``conf.py`` you can omit
   the ``-D version`` option to Sphinx build.

3. Run ``versjon`` in the common diretory - and you are done.

Customization
-------------
You can provide you own template for generating the version selector.

The easiest way is probably to copy the default ``src/templates/versjon.html``
one and adapt it. To use your own templates in Sphinx you need to add the
following to ``conf.py``::

    templates_path = ['mytemplate/wicked_versions.html']

Also you need to add the template e.g. to the ``html_sidebars`` list.

The `versjon.json` format
-------------------------

The ``versjon.json`` contains information about the different versions
generated. When you add the ``versjon`` extension to your Sphinx ``conf.py``
an initial ``versjon.json`` file will be generated everytime you build
your project.

As an example the initial versjon.json file could contain the following
information::

    {
        'format': 1,
        'current': '5.1.2',
        'all': [
            {'version': '5.1.2', 'path': '.'}
        ]
    }

There are three keys:

* ``format``: This is the version of the ``versjon`` JSON format :) It allows
   the ``verjson`` tool to output JSON that is compatible with older versions (
   we don't do that atm. but now we have the mechanism).
* ``current``: This is the actual project version specified the Sphinx
  configuration: https://www.sphinx-doc.org/en/master/usage/configuration.html
* ``all``: This contains a list of all ``versjon`` generated versions and a
  relative path to them (useful for generating links in the documentation).

  Inside the list we have a dictionary contaning ``version`` and ``path`` keys.
  The list is sorted such that non-semver versions appear first followed by
  semver versions (newest first).

After running ``sphinx-build`` on the versions you want to have included,
the ``versjon`` tool can traverse the folders and update the ``versjon.json``
file with links to the additional versions.

As an example after running the ``versjon`` tool a ``versjon.json`` file could
look something like::

    {
        'format': 1,
        'current': '1.0.0',
        'all': [
            {'version': 'latest', 'path': '../latest'}
            {'version': '2.0.0', 'path': '../2.0.0'}
            {'version': '1.0.0', 'path': '.'},
        ]
    }
