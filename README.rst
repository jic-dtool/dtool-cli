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
function of interest in the ``setup.py`` file.  Below is the content of a
hypothetical ``dtool_create/__init__.py`` file::

    import click

    @click.command()
    def create():
        print("Creating dataset...")

    @click.command()
    def freeze():
        print("Freezing dataset...")


To create an entry point for this function add the below in the ``setup.py``::

    from setuptools import setup

    setup(
        ...
        entry_points={
            "dtool.cli": [
                "create=dtool_create:create",
                "freeze=dtool_create:freeze",
            ],
        },
        ...
    )



Installation
------------

To install the dtool-cli package.

.. code-block:: bash

    cd dtool-cli
    python setup.py install
