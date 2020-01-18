#! /usr/bin/env python
# encoding: utf-8

import os
import json
import versjon


def test_run(testdirectory):

    project = testdirectory.copy_dir(directory="test/data/test_project")

    project.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.0.0 build_1.0.0')

    project.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.1.0 build_1.1.0')

    project.run(
        'sphinx-build --no-color -vvv -b html . -D version=2.0.0 build_2.0.0')

    project.run(
        'sphinx-build --no-color -vvv -b html . -D version=master build_master')

    r = project.run('versjon')
    print(r)

    assert 0
