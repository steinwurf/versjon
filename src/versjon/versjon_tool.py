#! /usr/bin/env python
# encoding: utf-8


import json
import os
import pathlib
import pickle
import sphobjinv
import bs4
import functools

import semantic_version as semver

from . import template_render


def current_version(build_dir):
    """ Return the current version of an objects.inv file"""

    objects_file = build_dir.joinpath('objects.inv')

    inventory = sphobjinv.Inventory(objects_file)

    if not inventory.version:
        raise RuntimeError(
            f'The versjon tool requires a version number '
            'in the {objects_file.parent}. Add one to conf.py or pass '
            'it to sphinx build using "-D version=X.Y.Z".')

    return inventory.version


def find_builds(docs_dir):
    """ Find all the available Sphinx builds in the documentation directory.

    We basically look for an file created by all Sphinx builds called:
    objects.inv

    :param docs_dir: The base directory contaning all the built docs
    :return: A list of pathlib.Path objects containing the path to each
        found build directory
    """
    return [build.parent for build in docs_dir.glob('**/objects.inv')]


def posix_path(from_dir, to_dir):
    """ Return the relative path between two directories """
    return pathlib.Path(os.path.relpath(path=to_dir, start=from_dir)).as_posix()


def create_context(docs_dir, from_build, to_builds):
    """ Create the context dictionary for a specific build

    See the README for the format.
    """

    current = current_version(from_build)

    # We rebuild the dictionary from scratch to avoid inconsistencies
    # from previous runs
    context = {
        'current': current,
        'is_semver': semver.validate(current),
        'stable': None,
        'semver': [],
        'other': [],
        'docs_path': {},
        'docs_root': None
    }

    for to_build in to_builds:
        print(f"Linking: {from_build} => {to_build}")

        # Get the version we are "pointing" to
        version = current_version(to_build)
        path = posix_path(from_dir=docs_dir, to_dir=to_build)

        # Store the version and its path in the all section
        context['docs_path'][version] = path

        if semver.validate(version):
            context['semver'].append(version)

        else:
            context['other'].append(version)

    # Sort all versions
    context['semver'] = sorted(
        context['semver'], key=lambda v: semver.Version(v), reverse=True)

    # Mark current stable release
    if context['semver']:
        context['stable'] = context['semver'][0]

    # Sort the non-semver versions
    context['other'] = sorted(context['other'])

    # Make sure that the master is listed first if in list
    context['other'] = sorted(context['other'], key=lambda v: v != 'master')

    return context


def run(docs_path):
    """ Run the versjon tool.

    :param docs_path: The path to the documentation as a string
    """
    # Transform to Path
    docs_path = pathlib.Path(docs_path)

    print(f'Running in {docs_path.resolve()}')

    # Get all the Sphinx builds in the the path
    builds = find_builds(docs_dir=docs_path)
    print(builds)

    # Our jinja2 template rendere use to geneate the HTML
    inject_render = template_render.TemplateRender(user_path=None)

    for build in builds:
        version = current_version(build)
        print(version)

        html_pages = list(build.glob('**/*.html'))

        context = create_context(
            docs_dir=docs_path, from_build=build, to_builds=builds)

        for html_page in html_pages:

            context['docs_root'] = posix_path(
                from_dir=html_page.parent, to_dir=docs_path) + '/'

            print(f"context => {context}")

            # Get the HTML to inject
            selector_data = inject_render.render(
                template_file='selector.html', context=context)

            style_data = inject_render.render(
                template_file='style.html', context={})

            warning_data = inject_render.render(
                template_file='warning.html', context=context)

            # Get the HTML for each page
            with open(html_page, 'r') as html_file:
                html_data = html_file.read()

            style = bs4.BeautifulSoup(style_data, features="html.parser")
            selector = bs4.BeautifulSoup(selector_data, features="html.parser")
            warning = bs4.BeautifulSoup(warning_data, features="html.parser")
            page = bs4.BeautifulSoup(html_data, features="html.parser")

            # Inject the HTML fragments in the .html page
            page.head.append(style)
            page.body.append(selector)
            page.body.insert(0, warning)

            print(f'Writing => {html_page}')

            with open(html_page, 'w') as html_file:
                html_file.write(str(page))
