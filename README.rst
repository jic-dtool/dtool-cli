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

To create a ``dtool-cli`` plug-in, create a Python package with entry points
along the lines of the below in the ``setup.py``::

    from setuptools import setup

    setup(
        ...
        entry_points={
            "dtool.dataset": [
                "create=dtool_create.cli:create_dataset",
                "markup=dtool_create.cli:markup_dataset",
                "manifest=dtool_create.cli:manifest",
            ],
            "dtool.collection": [
                "create=dtool_create.cli:create_collection",
                "markup=dtool_create.cli:markup_collection",
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
