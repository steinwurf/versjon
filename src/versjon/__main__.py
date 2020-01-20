#! /usr/bin/env python
# encoding: utf-8


import click
import pathlib
import os
import sys
import json
import semantic_version as semver


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
            'format': 1, 'current': current, 'semver': [], 'other': []}

        for to_path in versjons:
            print(f"{from_path.parent} => {to_path.parent}")

            # Get the version we are "pointing" to
            version = current_version(to_path)

            # We want the relative path from the directory containing the
            # versjon.json not the verjson.json file itself.
            path = os.path.relpath(
                path=to_path.parent, start=from_path.parent)

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


if __name__ == "__main__":
    cli()
