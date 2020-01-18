import os
import json

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

    We store the "version" value specified in the Sphinx
    configuration: https://www.sphinx-doc.org/en/master/usage/configuration.html

    In addition to this we store the path to the build folder. For the current
    Sphinx build the path will bhe '.'.

    As an example the initial versjon.json file could contain the following
    information:

        [
            {'version': '1.0.0', 'path': '.'}
        ]

    You can override the version variable in the configuration
    when running sphinx-build:

        sphinx-build... -D version=2.0.0 ...

    After running sphinx-build on the versions you want to have included,
    the versjon tool can traverse the folders and update the versjon.json
    file with links to the additional versions.

    As an example after running the versjon tool a versjon.json file could
    look something like:

        [
            {'version': 'latest', 'path': '../latest'}
            {'version': '1.0.0', 'path': '.'},
            {'version': '2.0.0', 'path': '../2.0.0'}
        ]

    The versjon.json then loaded by the HTML templates to generate version
    selectors and links.

    :param app: The application object, which is an instance of Sphinx.
    """

    versjon = [{'version': app.config.version, 'path': '.'}]

    with open(os.path.join(app.outdir, 'versjon.json'), 'w') as json_file:
        json.dump(versjon, json_file, indent=4, sort_keys=True)


def inject_sidebar(app, config):
    """ Injects the verjson.html to the html_sidebar"""

    if not config['versjon_inject_sidebar']:
        return

    #print("SIDEBARS {}".format(config['html_sidebars']))

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

    # Add the versjon configuration values
    app.add_config_value(name='versjon_inject_sidebar',
                         default=True, rebuild=True)

    # Generate the versjon.json
    app.connect(event="builder-inited", callback=write_versjon)
    app.connect(event="config-inited", callback=inject_sidebar)

    # We use the doctreedir as build directory. The default for this
    # is inside _build/.doctree folder
    # build_dir = os.path.join(app.doctreedir, 'wurfapi')

    return {'version': VERSION}
