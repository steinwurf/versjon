#! /usr/bin/env python
# encoding: utf-8

import os
import versjon

def test_versions(testdirectory):
    root = testdirectory.mkdir('root')

    expected_versions = [
        'latest', '12.11.0', '12.10.9',
        '12.0.0', '4.0.0', '3.0.0', '1.0.0',
        '0.0.1', '0.0.0', 'another-testing-branch',
        'some-testing-branch']

    for expected_version in expected_versions:
        root.mkdir(expected_version)
    print(os.listdir(root.path()))

    versions = versjon.versions(
        root.path(), 'http://127.0.0.1:8080/root/{version}.html')
    print(" ".join([version['name'] for version in versions]))

    for expected_version, version in zip(expected_versions, versions):
        assert expected_version == version['name']
        assert expected_version in version['url']

def test_write_json(testdirectory):
    versions = {'name': '1.0.0', 'url': 'some_url'}
    temp = testdirectory.mkdir('temp')
    versjon.write_json(versions, os.path.join(temp.path(), 'versions.json'))
    assert temp.contains_file('versions.json')
