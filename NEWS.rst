News for versjon
================

This file lists the major changes between versions. For a more detailed list of
every change, see the Git log.

Latest
------
* Minor: Updated waf.

2.1.0
-----
* Minor: Added support for an exclude_patten so that matched files will not be
  modified.

2.0.0
-----
* Major: Changed the general_context to allow links to keep their path when
  changing to another version. If a page doesn't exists at a specific version
  the link will simply go to the root.

1.1.1
-----
* Patch: Make page root relative for index page.

1.1.0
-----
* Minor: Added index file.

1.0.0
-----
* Major: Rewrote the tool to become what is described in README.
* Major: Supports Python 3.6 and up.
