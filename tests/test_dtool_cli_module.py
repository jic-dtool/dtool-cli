"""Test the dtool-cli package."""


def test_version_is_string():
    import dtool_cli
    assert isinstance(dtool_cli.__version__, str)
