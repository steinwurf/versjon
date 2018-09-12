#! /usr/bin/env python
# encoding: utf-8

import argparse
import os
import utils

def directory_check (string):
    if not os.path.exists(string):
        raise argparse.ArgumentTypeError("path does not exist: '{string}'".format(string=string))

    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("path is not a directory: '{string}'".format(string=string))

    return string

def cli():
    parser = argparse.ArgumentParser(description=
        'Creates a json file with version names based on a directory.')
    parser.add_argument(
        'directory',
        type=directory_check,
        help='The directory to base the version.json file on.')

    parser.add_argument('url_format', help=
		'''The format string for generating the url of the version.
		Example: "http://127.0.0.1/project/versions/{version}.html".
		Here {version} will be replaced with the name of the versions found in the directory.
		''')
    parser.add_argument('output', help='Output filename')

    args = parser.parse_args()

    versions = utils.versions(args.directory, args.url_format)
    utils.write_json(versions, args.output)


if __name__ == "__main__":
    cli()