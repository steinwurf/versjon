#! /usr/bin/env python
# encoding: utf-8


import click
import pathlib
import os
import sys
import json
import semantic_version as semver


def sort_versions(versions):
    """ Takes the "all" versions list and sorts it """

    # First we split versions into semver versions and non semver versions
    semver_versions = [v for v in versions if semver.validate(v['version'])]
    other_versions = [v for v in versions if v not in semver_versions]

    # Build the sorted list
    sorted_versions = []
    sorted_versions += sorted(other_versions, key=lambda v: v['version'])
    sorted_versions += sorted(semver_versions,
                              key=lambda v: semver.Version(v['version']),
                              reverse=True)

    return sorted_versions


def current_version(versjon_path):
    """ Return the current version of a versjon.json file"""
    with open(versjon_path) as json_file:
        data = json.load(json_file)
        return data['current']


@click.command()
@click.option('-d', '--docs_path', default='.')
def cli(docs_path):

    print(docs_path)

    # Transform to Path
    docs_path = pathlib.Path(docs_path)

    # Get all the versjon.json in the the path
    versjons = list(docs_path.glob('**/versjon.json'))

    # For each path visit all other paths
    for path_from in versjons:

        versjon_json = {'current': current_version(path_from), 'all': []}

        for path_to in versjons:
            print(f"{path_from.parent} => {path_to.parent}")

            # Get the version we are "pointing" to
            version = current_version(path_to)

            # We want the relative path from the directory containing the
            # versjon.json not the verjson.json file itself.
            path = os.path.relpath(
                path=path_to.parent, start=path_from.parent)

            # Store the version and its path in the all section
            versjon_json['all'].append({'version': version, 'path': path})

        # Sort all versions
        versjon_json['all'] = sort_versions(versjon_json['all'])

        with open(path_from, 'w') as json_file:
            json.dump(versjon_json, json_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    cli()
