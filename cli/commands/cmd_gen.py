import subprocess

import click

from src.database import get_db_url


@click.command()
def gen():
    """
    Runs Arbitrary Scripts from Scripts Folder

    Arguments:
        name {[type]} -- filename without ext
    """

    folder = "src"
    tables = "--tables reddit_memes"
    cmd = f"sqlacodegen {tables} --outfile {folder}/site_tables.py {get_db_url()}"

    return subprocess.call(cmd, shell=True)
