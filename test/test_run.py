#! /usr/bin/env python
# encoding: utf-8

import os
import json
import pytest
import sphinx
import pathlib
import pytest_testdirectory

import versjon.versjon_tool


def _test_run(testdirectory, datarecorder):

    project_dir = testdirectory.copy_dir(directory="test/data/test_project")

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.0.0 build_1.0.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.1.0 build_1.1.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=2.0.0 build_2.0.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=master build_master')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=abc build_abc')

    r = project_dir.run('versjon')
    print(r)

    def record_json(project_dir, build_dir):

        json_file = os.path.join(project_dir.path(), build_dir, 'versjon.json')

        assert os.path.isfile(json_file)

        recording_file = os.path.join(
            'test', 'recordings', build_dir + '_versjon.json')

        datarecorder.record_file(
            data_file=json_file, recording_file=recording_file)

    record_json(project_dir=project_dir, build_dir='build_1.0.0')
    record_json(project_dir=project_dir, build_dir='build_1.1.0')
    record_json(project_dir=project_dir, build_dir='build_2.0.0')
    record_json(project_dir=project_dir, build_dir='build_master')


def _test_run_no_version(testdirectory):

    project = testdirectory.copy_dir(directory="test/data/test_project")

    with pytest.raises(pytest_testdirectory.runresulterror.RunResultError) as error:
        project.run('sphinx-build --no-color -vvv -b html . build')

    print(error.value.runresult)

    # Check if our error is somewhere in the output
    assert error.value.runresult.stderr.match(
        '*The versjon extension requires a version number*')


def setup_project(testdirectory):

    project_dir = testdirectory.copy_dir(directory="test/data/test_project")

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.0.0 build_1.0.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=1.1.0 build_1.1.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=2.0.0 build_2.0.0')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=master build_master')

    project_dir.run(
        'sphinx-build --no-color -vvv -b html . -D version=abc build_abc')

    return project_dir


def test_run(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory)

    r = project_dir.run('versjon -v')
    print(r)


def test_create_context(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory)

    docs_path = pathlib.Path(project_dir.path())

    builds = versjon.versjon_tool.find_builds(docs_dir=docs_path)

    for build in builds:

        context = versjon.versjon_tool.create_context(
            docs_dir=docs_path, from_build=build, to_builds=builds)

        datarecorder.record_data(
            data=context,
            recording_file=f'test/recordings/context_{build.name}.json')


def test_find_builds(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory)
    docs_dir = pathlib.Path(project_dir.path())

    builds = versjon.versjon_tool.find_builds(docs_dir=docs_dir)

    # Make the relative for the recording
    paths = [versjon.versjon_tool.posix_path(
        docs_dir, build) for build in builds]

    datarecorder.record_data(
        data=paths,
        recording_file=f'test/recordings/find_builds.json')
