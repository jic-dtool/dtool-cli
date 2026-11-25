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

- Errors of commands, e.g. of storage brokers, are reported as one line
  ("Error: ...") with exit code 1 instead of a traceback; ``dtool --debug``
  shows the traceback


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^


[0.7.2] - 2026-11-23
--------------------

Added
^^^^^

- GitHub Actions workflow that publishes a release to PyPI when a version
  tag is pushed

Changed
^^^^^^^

- Build system switched to hatchling with hatch-vcs; the version is now
  derived from git tags
- Replaced ``pkg_resources`` entry-point discovery with
  ``importlib.metadata``, removing the ``pkg_resources`` deprecation warning

Removed
^^^^^^^

- Dropped support for Python < 3.10 (including Python 2)

Fixed
^^^^^

- The ``--version`` text is only built when ``--version`` is given. Previously
  it was built on import, so every ``dtool`` invocation imported all plugins,
  and a single plugin without ``__version__`` (or one that failed to import)
  broke the whole ``dtool`` command, including ``--help``; this also broke
  frozen (e.g. PyInstaller) builds
- A plugin or storage broker without ``__version__`` is listed with version
  "unknown" instead of crashing ``dtool --version``


[0.7.1] - 2021-06-23
--------------------

Fixed
^^^^^

- Licence file now included in release thanks to Jan Janssen (https://github.com/jan-janssen)


[0.7.0] - 2018-05-18
--------------------

Added
^^^^^

- Added support for ``-h`` flag as well as ``--help``
- Added timestamp to logging output

Fixed
^^^^^

- Improved handling of URIs in validation code


[0.6.0] - 2017-09-25
--------------------

Added
^^^^^

- ``dtool_cli.cli.base_dataset_uri_validation`` helper parameter validation method
- ``dtool_cli.cli.base_dataset_uri_argument`` helper decorator
- ``dtool_cli.cli.proto_dataset_uri_validation`` helper parameter validation method
- ``dtool_cli.cli.proto_dataset_uri_argument`` helper decorator

Changed
^^^^^^^

- ``dtool_cli.cli.dataset_uri_validation`` now validates that dataset is frozen
- ``dtool_cli.cli.dataset_uri_argument`` now validates that the dataset is frozen


[0.5.0] - 2017-09-20
--------------------

Changed
^^^^^^^

- Improved version string


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
