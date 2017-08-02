"""Skeleton defining the dtool plugin entry points."""

import os
from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

import dtoolcore


def _path_is_dataset(ctx, param, value):
    abspath = os.path.abspath(value)
    if not os.path.isdir(abspath):
        raise click.BadParameter(
            "Not a directory: {}".format(abspath))
    try:
        dtoolcore.DataSet.from_path(abspath)
    except (dtoolcore.DtoolTypeError, dtoolcore.NotDtoolObject) as e:
        raise click.BadParameter(
            "Not a dataset: {}".format(e))
    return abspath



dataset_path_argument = click.argument(
    'dataset_path',
    callback=_path_is_dataset)


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
