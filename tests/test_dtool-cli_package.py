"""Test the dtool-cli package."""


def test_version_is_string():
    import dtool-cli
    assert isinstance(dtool-cli.__version__, str)
