README
======

Data management command line interface: dtool.

Overview
--------

The ``dtool-cli`` python package provides a skeleton command line interface to
dtool that other "dtool" command line packages can be plugged into.

It makes use of `click <https://github.com/pallets/click>`_ and `click-plugins
<https://github.com/click-contrib/click-plugins>`_.


Creating a plugin
-----------------

The ``dtool-cli`` plug-in system exposes two name spaces for registering commands:

- ``dtool.dataset``
- ``dtool.collection``

To create a ``dtool-cli`` plug-in, create a Python package with a ``dataset``
and/or a ``collection`` module(s). Below is the content of a hypothetical
``dtool_create/dataset.py`` file, aka the ``dataset`` module in a
``dtool-create`` plugin::

    """dataset command line module."""

    import click


    @click.command()
    def create():
        print("Creating dataset...")


Then create entry points along the lines of the below in the ``setup.py``::

    from setuptools import setup

    setup(
        ...
        entry_points={
            "dtool.dataset": [
                "create=dtool_create.dataset:create",
                "markup=dtool_create.dataset:markup",
                "manifest=dtool_create.dataset:manifest",
            ],
            "dtool.collection": [
                "create=dtool_create.collection:create",
                "markup=dtool_create.collection:markup",
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
