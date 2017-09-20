CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Added
^^^^^


Changed
^^^^^^^

- Improved version string


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^


[0.4.0] - 2017-09-15
--------------------

Added
^^^^^

- ``dtool_cli.cli.storagebroker_validation`` helper parameter validation method


[0.3.0] - 2017-09-13
--------------------

Added
^^^^^

- ``dtool_cli.cli.dataset_uri_validation`` helper parameter validation method
- ``dtool_cli.cli.dataset_uri_argument`` helper decorator
- ``dtool_cli.cli.CONFIG_PATH`` global variable
- Add ``--debug`` option


[0.2.0] - 2017-08-30
--------------------

Basic scaffold to create a ``dtool`` client that uses the ``dtoolcore`` version
2 API.

Added
^^^^^

- Entry point for ``dtool.cli``

Removed
^^^^^^^

- Entry points ``dtool.dataset`` and ``dtool.collection``
