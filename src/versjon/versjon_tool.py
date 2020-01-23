#! /usr/bin/env python
# encoding: utf-8


import json
import os
import pathlib
import pickle
import sphobjinv

import semantic_version as semver


def _current_version(versjon_path):
    """ Return the current version of a versjon.json file"""
    with open(versjon_path) as json_file:
        data = json.load(json_file)
        return data['current']


def _run(docs_path):
    """ Run the versjon tool.

    :param docs_path: The path to the documentation as a string
    """
    print(f'Running in {docs_path}')

    # Transform to Path
    docs_path = pathlib.Path(docs_path)

    # Get all the versjon.json in the the path
    versjons = list(docs_path.glob('**/versjon.json'))

    if not versjons:
        raise RuntimeError(f'No versjon.json files found in {docs_path}.')

    # For each path visit all other paths
    for from_path in versjons:

        # Get the current version
        current = current_version(from_path)

        # We rebuild the json file from scratch to avoid inconsistencies if
        # the verjson.json files contain information from previous runs
        versjon_json = {
            'format': 1, 'current': current, 'semver': [], 'other': []}

        for to_path in versjons:
            print(f"{from_path.parent} => {to_path.parent}")

            # Get the version we are "pointing" to
            version = current_version(to_path)

            # We want the relative path from the directory containing the
            # versjon.json not the verjson.json file itself.
            path = pathlib.Path(os.path.relpath(
                path=to_path.parent, start=from_path.parent)).as_posix()

            # Store the version and its path in the all section
            if semver.validate(version):

                versjon_json['semver'].append(
                    {'version': version, 'path': path})

            else:

                versjon_json['other'].append(
                    {'version': version, 'path': path})

        # Sort all versions
        versjon_json['semver'] = sorted(
            versjon_json['semver'], key=lambda v: semver.Version(v['version']),
            reverse=True)

        versjon_json['other'] = sorted(
            versjon_json['other'], key=lambda v: v['version'])

        with open(from_path, 'w') as json_file:
            json.dump(versjon_json, json_file, indent=4, sort_keys=True)


def _1current_version(pickle_file):
    """ Return the current version of an environment.pickle file"""
    with open(pickle_file, 'rb') as file_object:
        pickle_data = pickle.load(file_object)

        # The pickle_data is a sphinx.environment.BuildEnvironment object. One
        # of the members is a sphinx.Config object, which contains the version
        # used in conf.py or during sphinx-build.

        return pickle_data.config['version']


def rewrite_html(path, versjon):

    html_pages = list(path.glob('**/*.html'))

    print(html_pages)


def _1run(docs_path):
    """ Run the versjon tool.

    :param docs_path: The path to the documentation as a string
    """
    # Transform to Path
    docs_path = pathlib.Path(docs_path)

    print(f'Running in {docs_path.resolve()}')

    # Get all the Sphinx builds in the the path
    builds = list(docs_path.glob('**/environment.pickle'))

    print(builds)

    for from_path in builds:

        # Get the current version
        current = current_version(from_path)

        if not current:
            raise RuntimeError(
                f'The versjon tool requires a version number '
                'in the {from_path}. Add one to conf.py or pass '
                'it to sphinx build using "-D version=X.Y.Z".')

        # We rebuild the dictionary from scratch to avoid inconsistencies
        # from previous runs
        versjon = {
            'format': 1, 'current': current, 'semver': [], 'other': []}

        for to_path in builds:
            print(f"{from_path.parents[1]} => {to_path.parents[1]}")

            # Get the version we are "pointing" to
            version = current_version(to_path)

            # We want the relative path from the build directory containing
            # the environement.pickle. Which should be in:
            #
            #    build/.doctrees/environement.pickle
            #
            # We want the obtain:
            #
            #    build/
            #
            path = pathlib.Path(os.path.relpath(
                path=to_path.parents[1], start=from_path.parents[1])).as_posix()

            # Store the version and its path in the all section
            if semver.validate(version):

                versjon['semver'].append(
                    {'version': version, 'path': path})

            else:

                versjon['other'].append(
                    {'version': version, 'path': path})

        # Sort all versions
        versjon['semver'] = sorted(
            versjon['semver'], key=lambda v: semver.Version(v['version']),
            reverse=True)

        versjon['other'] = sorted(
            versjon['other'], key=lambda v: v['version'])

        rewrite_html(path=from_path, versjon=versjon)


def current_version(objects_file):
    """ Return the current version of an objects.inv file"""
    inv = sphobjinv.Inventory(objects_file)

    print

    return inv.version


def run(docs_path):
    """ Run the versjon tool.

    :param docs_path: The path to the documentation as a string
    """
    # Transform to Path
    docs_path = pathlib.Path(docs_path)

    print(f'Running in {docs_path.resolve()}')

    # Get all the Sphinx builds in the the path
    builds = list(docs_path.glob('**/objects.inv'))
    print(builds)

    for build in builds:
        version = current_version(build)
        print(version)

