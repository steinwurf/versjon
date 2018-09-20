#! /usr/bin/env python
# encoding: utf-8

import argparse
import json
import os
import re
import semantic_version as semver

def versions(base_path, selectors, url_format):
	if (type(selectors) is not list):
		selectors = [selectors]

	base_path = os.path.abspath(os.path.expanduser(base_path))
	results = []

	for root, _, _ in os.walk(base_path):
		path = os.path.relpath(root, base_path)
		if any([re.match(selector, path) for selector in selectors]):
			results.append({
				'name': os.path.basename(path),
				'url': url_format.format(path=path)
			})
	semver_versions = [r for r in results if semver.validate(r['name'])]
	non_semver = [r for r in results if r not in semver_versions]
	sorted_results = []
	sorted_results += sorted(non_semver, key=lambda k: k['name'])
	sorted_results += sorted(semver_versions, key=lambda k: semver.Version(k['name']), reverse=True)
	return sorted_results

def write_json(versions, output):
	with open(output, 'w') as outfile:
		json.dump(versions, outfile, indent=2, sort_keys=True)
