import os
import json

import semantic_version as semver

import sphinx
import sphinx.util
import sphinx.util.logging
import sphinx.builders
import sphinx.builders.html
import sphinx.application
import sphinx.theming

VERSION = '0.0.0'


def write_versjon(app):
    """ Writes the versjon.json to the build folder.

    :param app: The application object, which is an instance of Sphinx.
    """

    # The version specified in Sphinx
    version = app.config.version

    versjon = {'format': 1, 'current': version, 'semver': [], 'other': []}

    if semver.validate(version):
        versjon['semver'].append({'version': version, 'path': '.'})
    else:
        versjon['other'].append({'version': version, 'path': '.'})

    with open(os.path.join(app.outdir, 'versjon.json'), 'w') as json_file:
        json.dump(versjon, json_file, indent=4, sort_keys=True)


def inject_templates_path(app, config):
    """ Injects our templates_path such that we can use it in html_sidebars"""

    config['templates_path'].append(os.path.join(
        os.path.dirname(__file__), 'templates'))


def setup(app):
    """ Entry point for the extension.

    Sphinx will call this function when the
    module is added to the "extensions" list in Sphinx's conf.py file.

    :param app: The application object, which is an instance of Sphinx.
    """

    # Create a logger
    logger = sphinx.util.logging.getLogger('versjon')
    logger.info('Initializing versjon extension')

    # Generate the versjon.json
    app.connect(event="builder-inited", callback=write_versjon)
    app.connect(event="config-inited", callback=inject_templates_path)

    return {'version': VERSION}
