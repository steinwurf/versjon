#! /usr/bin/env python
# encoding: utf-8

import os
import waflib

top = '.'

VERSION = '0.0.0'


def options(opt):

    opt.add_option(
        '--run_tests', default=False, action='store_true',
        help='Run all unit tests')

    opt.add_option(
        '--pytest_basetemp', default='pytest_temp',
        help='Set the prefix folder where pytest executes the tests')

def configure(conf):
    pass


def build(bld):

    # Create a virtualenv in the source folder and build universal wheel
    # Make sure the virtualenv Python module is in path
    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:
        venv.pip_install(packages=['wheel'])
        venv.run(cmd='python setup.py bdist_wheel --universal', cwd=bld.path)

    # Delete the egg-info directory, do not understand why this is created
    # when we build a wheel. But, it is - perhaps in the future there will
    # be some way to disable its creation.
    egg_info = os.path.join('src', 'versjon.egg-info')

    if os.path.isdir(egg_info):
        waflib.extras.wurf.directory.remove_directory(path=egg_info)

    # Run the unit-tests
    if bld.options.run_tests:
        _pytest(bld=bld)


def _pytest(bld):

    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:

        # If we need to be able to run doxygen from the system
        venv.env['PATH'] = os.path.pathsep.join(
            [venv.env['PATH'], os.environ['PATH']])

        venv.pip_install(['pytest', 'pytest-testdirectory'])

        # Install the pytest-testdirectory plugin in the virtualenv
        # Find the .whl file in the dist folder.

        wheel = bld.path.ant_glob('dist/*-'+VERSION+'-*.whl')

        if not len(wheel) == 1:
            bld.fatal('No wheel found (or version mismatch)')
        wheel = wheel[0]

        venv.run('python -m pip install {}'.format(wheel))

        # We override the pytest temp folder with the basetemp option,
        # so the test folders will be available at the specified location
        # on all platforms. The default location is the "pytest" local folder.
        basetemp = os.path.abspath(os.path.expanduser(
            bld.options.pytest_basetemp))

        # We need to manually remove the previously created basetemp folder,
        # because pytest uses os.listdir in the removal process, and that fails
        # if there are any broken symlinks in that folder.
        if os.path.exists(basetemp):
            waflib.extras.wurf.directory.remove_directory(path=basetemp)

        testdir = bld.path.find_node('test')

        # Make the basetemp directory
        os.makedirs(basetemp)

        # Main test command
        command = 'python -B -m pytest {} --basetemp {}'.format(
            testdir.abspath(), os.path.join(basetemp, 'unit_tests'))

        # Make python not write any .pyc files. These may linger around
        # in the file system and make some tests pass although their .py
        # counter-part has been e.g. deleted
        venv.run(cmd=command, cwd=bld.path)
