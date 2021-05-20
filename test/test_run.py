#! /usr/bin/env python
# encoding: utf-8

import os
import json
import pytest
import sphinx
import pathlib
import pytest_testdirectory

import versjon.versjon_tool


def setup_project(testdirectory, include_semver=True):

    project_dir = testdirectory.copy_dir(directory="test/data/test_project")

    if include_semver:
        project_dir.run(
            "sphinx-build --no-color -vvv -b html . -D version=1.0.0 build_1.0.0"
        )

        project_dir.run(
            "sphinx-build --no-color -vvv -b html . -D version=1.1.0 build_1.1.0"
        )

        project_dir.run(
            "sphinx-build --no-color -vvv -b html . -D version=2.0.0 build_2.0.0"
        )

    project_dir.run(
        "sphinx-build --no-color -vvv -b html . -D version=master build_master"
    )

    project_dir.run("sphinx-build --no-color -vvv -b html . -D version=abc build_abc")

    return project_dir


def test_run(testdirectory):

    project_dir = setup_project(testdirectory)

    r = project_dir.run("versjon -v")
    print(r)


def test_create_general_context(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory)

    docs_path = pathlib.Path(project_dir.path())

    builds = versjon.versjon_tool.find_builds(docs_dir=docs_path)

    context = versjon.versjon_tool.create_general_context(
        docs_dir=docs_path, builds=builds
    )

    datarecorder.record_data(
        data=context, recording_file=f"test/recordings/general_context.json"
    )


def test_find_builds(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory)
    docs_dir = pathlib.Path(project_dir.path())

    builds = versjon.versjon_tool.find_builds(docs_dir=docs_dir)

    # Make the relative for the recording
    paths = [versjon.versjon_tool.posix_path(docs_dir, build) for build in builds]

    datarecorder.record_data(
        data=sorted(paths), recording_file="test/recordings/find_builds.json"
    )


def test_files(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory)
    r = project_dir.run(f"versjon --docs_path {project_dir}")
    assert project_dir.contains_dir("build_1.0.0")
    assert project_dir.contains_dir("build_1.1.0")
    assert project_dir.contains_dir("build_2.0.0")
    assert project_dir.contains_dir("build_abc")
    assert project_dir.contains_dir("build_master")
    assert project_dir.contains_dir("stable")
    assert project_dir.contains_file("index.html")
    assert project_dir.contains_file("stable/index.html")

    datarecorder.record_file(
        data_file=os.path.join(project_dir.path(), "index.html"),
        recording_file="test/recordings/index.html",
    )

    datarecorder.record_file(
        data_file=os.path.join(project_dir.path(), "stable/index.html"),
        recording_file="test/recordings/stable_index.html",
    )


def test_files_no_semver(testdirectory, datarecorder):

    project_dir = setup_project(testdirectory, include_semver=False)
    r = project_dir.run(f"versjon --docs_path {project_dir}")
    assert project_dir.contains_dir("build_abc")
    assert project_dir.contains_dir("build_master")
    assert not project_dir.contains_dir("stable")
    assert project_dir.contains_file("index.html")

    datarecorder.record_file(
        data_file=os.path.join(project_dir.path(), "index.html"),
        recording_file="test/recordings/no_semver_index.html",
    )
