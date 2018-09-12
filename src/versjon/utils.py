#! /usr/bin/env python
# encoding: utf-8

import argparse
import json
import os
import semantic_version as semver

def versions(root, url_format):
	files = os.listdir(root)
	directories = set([f for f in files if os.path.isdir(os.path.join(root, f))])

	valid_versions = set([directory for directory in directories if semver.validate(directory)])
	invalid_versions = directories - valid_versions

	versions = []
	if 'latest' in invalid_versions:
		versions += ['latest']
		invalid_versions = invalid_versions - set(['latest'])

	versions += sorted(valid_versions, key=semver.Version, reverse=True)
	versions += sorted(invalid_versions)

	results = []
	for version in versions:
		url = url_format.format(version=version)
		results.append({ 'name': version, 'url': url })
	return results

def write_json(versions, output):
	with open(output, 'w') as outfile:
		json.dump(versions, outfile, indent=2, sort_keys=True)
