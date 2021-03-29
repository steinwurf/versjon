#! /usr/bin/env python
# encoding: utf-8


import click
import colorama
import sys

from .versjon_tool import run


@click.command()
@click.option('-d', '--docs_path', default='.')
@click.option('-e', '--exclude_pattern', default=None)
@click.option('-v', '--verbose', is_flag=True)
@click.option('-i', '--no_index', is_flag=True)
@click.option('-s', '--no_stable_index', is_flag=True)
@click.option('-u', '--user_templates', default=None)
def cli(docs_path, exclude_pattern, verbose, no_index, no_stable_index, user_templates):
    try:
        run(docs_path=docs_path, exclude_pattern=exclude_pattern, no_index=no_index,
            no_stable_index=no_stable_index, user_templates=user_templates)
    except Exception as e:

        if verbose:
            # We just propagate the exception out
            raise

        colorama.init()
        print(colorama.Fore.RED + str(e))
        sys.exit(1)


if __name__ == "__main__":
    cli()
