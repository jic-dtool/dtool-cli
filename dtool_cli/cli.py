"""Skeleton defining the dtool plugin entry points."""

import os
from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

import dtoolcore

from . import __version__


def _path_is_dataset(ctx, param, value):
    abspath = os.path.abspath(value)
    if not os.path.isdir(abspath):
        raise click.BadParameter(
            "Not a directory: {}".format(abspath))
    try:
        dtoolcore.DataSet.from_uri(abspath)
    except dtoolcore.DtoolCoreTypeError as e:
        try:
            dtoolcore.ProtoDataSet.from_uri(abspath)
        except dtoolcore.DtoolCoreTypeError as e:
            raise click.BadParameter(
                "Not a dataset: {}".format(e))
    return abspath


dataset_path_argument = click.argument(
    'dataset_path',
    callback=_path_is_dataset)


def pretty_version_text():
    """Return pretty version text listing all plugins."""
    modules = [ep.module_name for ep in iter_entry_points("dtool.dataset")]
    modules = modules + [ep.module_name for ep in iter_entry_points("dtool.collection")]
    packages = set([m.split(".")[0] for m in modules])
    version_lines = ["dtool, version {}".format(__version__)]
    version_lines.append("\nCore:")
    version_lines.append("dtoolcore, version {}".format(dtoolcore.__version__))
    version_lines.append("\nPlugins:")
    for p in packages:
        dyn_load_p = __import__(p)
        version_lines.append("{}, version {}".format(p,  dyn_load_p.__version__))
    return "\n".join(version_lines)

@click.group()
@click.version_option(message=pretty_version_text())
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
