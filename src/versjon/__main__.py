#! /usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

import argparse
import os
import sys
import versjon

def cli():
    parser = argparse.ArgumentParser(description=
        'Creates a json file with version names based on a a base path and a '
        'set of selectors.')

    parser.add_argument('--base_path', help='The base path.', default=r'.')

    parser.add_argument(
        'selectors',
        nargs='*',
        help=
            'A selector is a regex which will determine if a directory in the '
            'given base path')

    parser.add_argument('url_format', help=
		'''
        The format string for generating the url of the version.
        The generated string is based on the variable {path}.
        Path is the path to the selected directory.
		Sample url format string: "http://127.0.0.1/{path}".
		Here {path} will be replaced with the selected paths.
		''')

    parser.add_argument('output_file', help='The name of the output file.')
    args = parser.parse_args()

    versions = versjon.versions(args.base_path, args.selectors, args.url_format)
    versjon.write_json(versions, args.output_file)

if __name__ == "__main__":
    cli()
