#! /usr/bin/env python
# encoding: utf-8

import os
import json
import versjon

def test_versions(testdirectory):
    project = testdirectory.mkdir('project_name')
    docs = project.mkdir('docs')
    latest = docs.mkdir('latest')
    static = latest.mkdir('static')
    static.mkdir('tags').mkdir('10.0.0')
    static.mkdir('js')
    static.mkdir('css')
    tags = docs.mkdir('tags')
    one = tags.mkdir('0.2.10')
    one.mkdir('js')
    one.mkdir('css')
    two = tags.mkdir('2.10.9')
    two.mkdir('js')
    two.mkdir('css')
    ten = tags.mkdir('10.0.0')
    ten.mkdir('js')
    ten.mkdir('css')

    versions = versjon.versions(
        docs.path(),
        [r'latest$', r'tags/\d+\.\d+\.\d+$'],
        'http://127.0.0.1:8080/{path}')

    expectations = [
        { 'name': 'latest', 'url': 'http://127.0.0.1:8080/latest' },
        { 'name': '10.0.0', 'url': 'http://127.0.0.1:8080/tags/10.0.0' },
        { 'name': '2.10.9', 'url': 'http://127.0.0.1:8080/tags/2.10.9' },
        { 'name': '0.2.10', 'url': 'http://127.0.0.1:8080/tags/0.2.10' },
    ]

    assert len(versions) == len(expectations)

    for version, expectation in zip(versions, expectations):
        assert version['name'] == expectation['name']
        assert version['url'] == expectation['url']


    cmd = 'versjon --base_path {base_path} {selectors} {url_format} {output_file}'.format(
        base_path=docs.path(),
        selectors=' '.join([r'latest$', r'tags/\d+\.\d+\.\d+$']),
        url_format='http://127.0.0.1:8080/{path}',
        output_file='versions.json',
    )
    testdirectory.run(cmd)

    assert testdirectory.contains_file('versions.json')

    with open(os.path.join(testdirectory.path(), 'versions.json')) as f:
        read_versions = json.load(f)
        print(read_versions)
        for read_version, version in zip(read_versions, versions):
            assert read_version['name'] == version['name']
            assert read_version['url'] in version['url']

def test_write_json(testdirectory):
    versions = {'name': '1.0.0', 'url': 'some_url'}
    temp = testdirectory.mkdir('temp')
    versjon.write_json(versions, os.path.join(temp.path(), 'versions.json'))
    assert temp.contains_file('versions.json')
