#! /usr/bin/env python
# encoding: utf-8


import click
import colorama
import sys

from .versjon_tool import run


@click.command()
@click.option('-d', '--docs_path', default='.')
@click.option('-v', '--verbose', is_flag=True)
def cli(docs_path, verbose):
    try:
        run(docs_path=docs_path)
    except Exception as e:

        if verbose:
            # We just propagate the exception out
            raise

        colorama.init()
        print(colorama.Fore.RED + str(e))
        sys.exit(1)


if __name__ == "__main__":
    cli()
