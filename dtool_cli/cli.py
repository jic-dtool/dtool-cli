"""Skeleton defining the dtool plugin entry points."""

from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins


@click.group()
def dtool():
    """Manage data as datasets and collections."""


@with_plugins(iter_entry_points("dtool.dataset"))
@dtool.group()
def dataset():
    """Commands to work on a dataset."""


@with_plugins(iter_entry_points("dtool.collection"))
@dtool.group()
def collection():
    """Commands to work on a collection."""


if __name__ == "__main__":
    dtool()
