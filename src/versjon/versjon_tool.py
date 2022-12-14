#! /usr/bin/env python
# encoding: utf-8


import json
import fnmatch
import os
import pathlib
import pickle
import sphobjinv
import bs4
import functools

import semantic_version as semver

from . import template_render


def current_version(build_dir):
    """Return the current version of an objects.inv file"""

    objects_file = build_dir.joinpath("objects.inv")

    inventory = sphobjinv.Inventory(objects_file)

    if not inventory.version:
        raise RuntimeError(
            "The versjon tool requires a version number in the"
            f"'{objects_file.parent}' directory. Add one to conf.py or pass "
            'it to sphinx build using "-D version=X.Y.Z".'
        )

    return inventory.version


def find_builds(docs_dir):
    """Find all the available Sphinx builds in the documentation directory.

    We basically look for an file created by all Sphinx builds called:
    objects.inv

    :param docs_dir: The base directory contaning all the built docs
    :return: A list of pathlib.Path objects containing the path to each
        found build directory
    """
    return [build.parent for build in docs_dir.glob("**/objects.inv")]


def posix_path(from_dir, to_dir):
    """Return the relative path between two directories"""
    return pathlib.Path(os.path.relpath(path=to_dir, start=from_dir)).as_posix()


def create_general_context(docs_dir, builds):
    """Create the general context dictionary

    See the README for the format.
    """

    # We rebuild the dictionary from scratch to avoid inconsistencies
    # from previous runs
    context = {
        "stable": None,
        "semver": [],
        "other": [],
        "docs_path": {},
    }

    for build in builds:

        # Get the version we are "pointing" to
        version_name = current_version(build)
        path = posix_path(from_dir=docs_dir, to_dir=build)

        # Store the version and its path in the all section
        context["docs_path"][version_name] = path

        html_files = []
        for html_page in build.glob("**/*.html"):
            html_files.append(posix_path(from_dir=build, to_dir=html_page))

        version = {"name": version_name, "html_files": sorted(html_files)}

        if semver.validate(version_name):
            context["semver"].append(version)

        else:
            context["other"].append(version)

    # Sort all versions
    context["semver"] = sorted(
        context["semver"], key=lambda v: semver.Version(v["name"]), reverse=True
    )

    # Mark current stable release
    if context["semver"]:
        context["stable"] = context["semver"][0]

    # Sort the non-semver versions
    context["other"] = sorted(context["other"], key=lambda v: v["name"])

    # Make sure that the master is listed first if in list
    context["other"] = sorted(context["other"], key=lambda v: v["name"] != "master")

    # Make sure that the latest is listed first if in list
    context["other"] = sorted(context["other"], key=lambda v: v["name"] != "latest")

    if context["stable"] is not None:
        context["index"] = context["stable"]
    else:
        context["index"] = context["other"][0]

    return context


def run(docs_path, exclude_pattern, no_index, no_stable_index, user_templates):
    """Run the versjon tool.

    :param docs_path: The path to the documentation as a string
    :param exclude_pattern: Exclude pattern for files not to modify.
                            Uses Unix shell-style wildcards.
    """
    # Transform to Path
    docs_path = pathlib.Path(docs_path)

    print(f"Running in {docs_path.resolve()}")

    # Get all the Sphinx builds in the the path
    builds = find_builds(docs_dir=docs_path)
    print(builds)

    # Our jinja2 template rendere use to geneate the HTML
    inject_render = template_render.TemplateRender(user_path=user_templates)

    # Get the general context
    general_context = create_general_context(docs_dir=docs_path, builds=builds)

    for build in builds:

        current = current_version(build)

        # Build context
        build_context = {"current": current, "is_semver": semver.validate(current)}

        for html_page in build.glob("**/*.html"):

            page_root = posix_path(from_dir=html_page.parent, to_dir=docs_path) + "/"

            page = posix_path(from_dir=build, to_dir=html_page)

            if exclude_pattern is not None:
                if fnmatch.fnmatch(str(html_page), exclude_pattern):
                    print(f"Skipping => {html_page}")
                    continue

            # Page context
            page_context = {
                "page": page,
                "page_root": page_root,
            }

            print(f"context => {general_context}, {build_context}, {page_context}")

            # Get the HTML to inject
            head_data = inject_render.render(
                template_file="head.html",
                **general_context,
                **build_context,
                **page_context,
            )

            header_data = inject_render.render(
                template_file="header.html",
                **general_context,
                **build_context,
                **page_context,
            )

            footer_data = inject_render.render(
                template_file="footer.html",
                **general_context,
                **build_context,
                **page_context,
            )

            # Get the HTML for each page
            with open(html_page, "r") as html_file:
                html_data = html_file.read()

            head = bs4.BeautifulSoup(head_data, features="html.parser")
            header = bs4.BeautifulSoup(header_data, features="html.parser")
            footer = bs4.BeautifulSoup(footer_data, features="html.parser")
            page = bs4.BeautifulSoup(html_data, features="html.parser")

            # Inject the HTML fragments in the .html page
            page.head.append(head)

            page.body.insert(0, header)
            page.body.append(footer)

            print(f"Writing => {html_page}")

            with open(html_page, "w") as html_file:
                html_file.write(str(page))

    if not no_stable_index and general_context["stable"]:
        # We are pragmatic here and we bail if no stable version exist.
        # We could ask the user

        stable_dir = docs_path.joinpath("stable")

        if stable_dir.is_dir():
            # We assume no stable version has been generated if so, we should
            # not do it
            raise RuntimeError("stable directory already exists!")

        stable_dir.mkdir()

        page_context = {"page_root": "../"}

        index_data = inject_render.render(
            template_file="stable_index.html", **general_context, **page_context
        )

        with open(stable_dir.joinpath("index.html"), "w") as index_html:
            index_html.write(index_data)

    if not no_index:
        index_dir = docs_path

        page_context = {"page_root": "./"}

        index_data = inject_render.render(
            template_file="index.html", **general_context, **page_context
        )

        with open(index_dir.joinpath("index.html"), "w") as index_html:
            index_html.write(index_data)
