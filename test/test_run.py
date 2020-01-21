#! /usr/bin/env python
# encoding: utf-8

import os
import json
import pytest
import sphinx
import pytest_testdirectory


def test_run(testdirectory, datarecorder):

    project_dir = testdirectory.copy_dir(directory="test/data/test_project")

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.0.0 build_1.0.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.1.0 build_1.1.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=2.0.0 build_2.0.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=master build_master')

    r = project_dir.run('versjon')
    print(r)

    def record_json(project_dir, build_dir):
        assert project_dir.join(build_dir).contains_file('versjon.json')

    record_json(project_dir=project_dir, build_dir='build_1.0.0')
    record_json(project_dir=project_dir, build_dir='build_1.1.0')
    record_json(project_dir=project_dir, build_dir='build_2.0.0')
    record_json(project_dir=project_dir, build_dir='build_master')

    assert 0


def test_run_no_version(testdirectory):

    project = testdirectory.copy_dir(directory="test/data/test_project")

    with pytest.raises(pytest_testdirectory.runresulterror.RunResultError) as error:
        project.run('sphinx-build --no-color -vvv -b html . build')

    print(error.value.runresult)

    # Check if our error is somewhere in the output
    assert error.value.runresult.stderr.match(
        '*The versjon extension requires a version number*')
