"""Skeleton defining the dtool plugin entry points."""

import logging

from pkg_resources import iter_entry_points

import click
from click_plugins import with_plugins

import dtoolcore

from . import __version__


def pretty_version_text():
    """Return pretty version text listing all plugins."""
    version_lines = ["dtool, version {}".format(__version__)]
    version_lines.append("\nCore:")
    version_lines.append("dtoolcore, version {}".format(dtoolcore.__version__))

    # List the storage broker packages.
    version_lines.append("\nStorage brokers:")
    for ep in iter_entry_points("dtool.storage_brokers"):
        package = ep.module_name.split(".")[0]
        dyn_load_p = __import__(package)
        version = dyn_load_p.__version__
        storage_broker = ep.load()
        version_lines.append(
            "{}, {}, version {}".format(
                storage_broker.key,
                package,
                version))

    # List the plugin packages.
    modules = [ep.module_name for ep in iter_entry_points("dtool.cli")]
    packages = set([m.split(".")[0] for m in modules])
    version_lines.append("\nPlugins:")
    for p in packages:
        dyn_load_p = __import__(p)
        version_lines.append(
            "{}, version {}".format(p,  dyn_load_p.__version__))

    return "\n".join(version_lines)


@with_plugins(iter_entry_points("dtool.cli"))
@click.group()
@click.version_option(message=pretty_version_text())
@click.option("--debug", is_flag=True, help="Turn on debugging output.")
def dtool(debug):
    """Tool to work with datasets."""
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=level)
