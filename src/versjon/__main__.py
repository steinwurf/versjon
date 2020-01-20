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
    for from_path in versjons:

        # Get the current version
        current = current_version(from_path)

        # We rebuild the json file from scratch to avoid inconsistencies if
        # the verjson.json files contain information from previous runs
        versjon_json = {
            'format': 1, 'current': current, 'all': []}

        for to_path in versjons:
            print(f"{from_path.parent} => {to_path.parent}")

            # Get the version we are "pointing" to
            version = current_version(to_path)

            # We want the relative path from the directory containing the
            # versjon.json not the verjson.json file itself.
            path = os.path.relpath(
                path=to_path.parent, start=from_path.parent)

            # Store the version and its path in the all section
            versjon_json['all'].append({'version': version, 'path': path})

        # Sort all versions
        versjon_json['all'] = sort_versions(versjon_json['all'])

        with open(from_path, 'w') as json_file:
            json.dump(versjon_json, json_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    cli()
