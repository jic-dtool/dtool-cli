README
======

Data management command line tool: dtool.

Overview
--------

The ``dtool-cli`` python package provides a skeleton command line interface to
dtool that other "dtool" command line packages can be plugged into.

It makes use of `click <https://github.com/pallets/click>`_ and `click-plugins
<https://github.com/click-contrib/click-plugins>`_.


Creating a plugin
-----------------

The ``dtool-cli`` plug-in system exposes name space ``dtool.cli`` for
registering commands.


To create a ``dtool-cli`` plug-in, create a Python package and register the
click commands of interest as entry points in its ``pyproject.toml`` file.
Below is the content of a hypothetical ``dtool_create/__init__.py`` file::

    import click

    @click.command()
    def create():
        print("Creating dataset...")

    @click.command()
    def freeze():
        print("Freezing dataset...")


To create entry points for these commands add the below to the
``pyproject.toml``::

    [project.entry-points."dtool.cli"]
    create = "dtool_create:create"
    freeze = "dtool_create:freeze"

The entry points must refer to click commands (or groups). Plain functions,
e.g. ``argparse`` based scripts, belong under ``[project.scripts]`` instead.



Installation
------------

To install the dtool-cli package.

.. code-block:: bash

    cd dtool-cli
    pip install .
