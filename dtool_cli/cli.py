"""Skeleton defining the dtool plugin entry points."""

import os
import logging

from importlib.metadata import entry_points

import click
from click_plugins import with_plugins

import dtoolcore
import dtoolcore.utils

try:
    from dtool import __version__ as dtool_version
except ImportError:
    dtool_version = ""

from . import __version__

_CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CONFIG_PATH = os.path.expanduser("~/.config/dtool/dtool.json")


def iter_entry_points(group):
    """Yield the entry points registered under ``group``."""
    return entry_points(group=group)


def storagebroker_validation(ctx, param, value):
    storage_broker_lookup = dtoolcore._generate_storage_broker_lookup()
    if value not in storage_broker_lookup:
        raise click.BadParameter(
            "'{}' not in {}".format(value, storage_broker_lookup.keys()))
    return value


def base_dataset_uri_validation(ctx, param, value):
    value = dtoolcore.utils.sanitise_uri(value)
    if not dtoolcore._is_dataset(value, config_path=CONFIG_PATH):
        raise click.BadParameter(
            "URI is not a dataset: {}".format(value))
    return value


def proto_dataset_uri_validation(ctx, param, value):
    value = base_dataset_uri_validation(ctx, param, value)
    admin_metadata = dtoolcore._admin_metadata_from_uri(
        uri=value,
        config_path=CONFIG_PATH
    )
    if admin_metadata["type"] != "protodataset":
        message_lines = [
            "\nURI is not a proto dataset: {}".format(value),
            "It looks like a frozen dataset",
        ]
        raise click.BadParameter("\n".join(message_lines))
    return value


def dataset_uri_validation(ctx, param, value):
    value = base_dataset_uri_validation(ctx, param, value)
    admin_metadata = dtoolcore._admin_metadata_from_uri(
        uri=value,
        config_path=CONFIG_PATH
    )
    if admin_metadata["type"] != "dataset":
        message_lines = [
            "\nURI is not a frozen dataset: {}".format(value),
            "It looks like a proto dataset",
        ]
        raise click.BadParameter("\n".join(message_lines))
    return value


base_dataset_uri_argument = click.argument(
    "dataset_uri",
    callback=base_dataset_uri_validation
)


proto_dataset_uri_argument = click.argument(
    "proto_dataset_uri",
    callback=proto_dataset_uri_validation
)


dataset_uri_argument = click.argument(
    "dataset_uri",
    callback=dataset_uri_validation
)


def _package_version(package):
    """Return the ``__version__`` of ``package``, or "unknown".

    A plugin that cannot be imported or that lacks ``__version__`` must not
    break the version listing.
    """
    try:
        return __import__(package).__version__
    except Exception:
        return "unknown"


def _storage_broker_key(ep):
    """Return the key of the storage broker behind entry point ``ep``."""
    try:
        return ep.load().key
    except Exception:
        return ep.name


def pretty_version_text():
    """Return pretty version text listing all plugins."""
    version_lines = ["dtool, version {}".format(dtool_version)]
    version_lines.append("\nBase:")
    version_lines.append("dtoolcore, version {}".format(dtoolcore.__version__))
    version_lines.append("dtool-cli, version {}".format(__version__))

    # List the storage broker packages.
    version_lines.append("\nStorage brokers:")
    for ep in iter_entry_points("dtool.storage_brokers"):
        package = ep.module.split(".")[0]
        version_lines.append(
            "{}, {}, version {}".format(
                _storage_broker_key(ep),
                package.replace("_", "-"),
                _package_version(package)))

    # List the plugin packages.
    modules = [ep.module for ep in iter_entry_points("dtool.cli")]
    packages = set([m.split(".")[0] for m in modules])
    version_lines.append("\nPlugins:")
    for p in packages:
        version_lines.append(
            "{}, version {}".format(
                p.replace("_", "-"),
                _package_version(p)))

    return "\n".join(version_lines)


def _print_version(ctx, param, value):
    """Print the version of dtool and its plugins, then exit.

    The text is only built when ``--version`` is given: building it imports
    every plugin, which should neither slow down nor be able to break other
    invocations of ``dtool``.
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo(pretty_version_text())
    ctx.exit()


class _DtoolGroup(click.Group):
    """Report errors of commands as one line instead of a traceback.

    Errors of storage brokers and dtoolcore (e.g. "Not logged in", a
    missing bucket) are not bugs of the command line; ``dtool --debug``
    shows the traceback.
    """

    def invoke(self, ctx):
        try:
            return super().invoke(ctx)
        except (click.exceptions.ClickException, click.exceptions.Exit,
                click.exceptions.Abort):
            raise
        except Exception as e:
            if ctx.params.get("debug"):
                raise
            message = str(e) or type(e).__name__
            raise click.ClickException(
                f"{message}\n(Run 'dtool --debug ...' for details.)"
            ) from e


@with_plugins(iter_entry_points("dtool.cli"))
@click.group(cls=_DtoolGroup, context_settings=_CLICK_CONTEXT_SETTINGS)
@click.option("--version", is_flag=True, expose_value=False, is_eager=True,
              callback=_print_version, help="Show the version and exit.")
@click.option("--debug", is_flag=True, help="Turn on debugging output.")
def dtool(debug):
    """Tool to work with datasets."""
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level)
