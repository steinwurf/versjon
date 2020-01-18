#! /usr/bin/env python
# encoding: utf-8

import os
import json
import versjon


def test_run(testdirectory):

    project = testdirectory.copy_dir(directory="test/data/test_project")

    r = project.run('sphinx-build --no-color -w log.txt -vvv -b html . _build')
    print(r)
    assert 0
