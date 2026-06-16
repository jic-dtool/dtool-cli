"""Test the dtool-cli package."""

from click.testing import CliRunner


def test_version_is_string():
    import dtool_cli
    assert isinstance(dtool_cli.__version__, str)


def test_dtool():
    from dtool_cli.cli import dtool
    runner = CliRunner()
    result = runner.invoke(dtool, ["--help"])
    assert result.exit_code == 0


def test_dtool_debug_flag():
    # Attach a throwaway subcommand so the group callback body actually runs
    # (--help would short-circuit before it). This exercises the --debug branch
    # that switches logging to DEBUG.
    import click
    from dtool_cli.cli import dtool

    @dtool.command(name="_noop")
    def _noop():
        click.echo("ran")

    try:
        runner = CliRunner()
        result = runner.invoke(dtool, ["--debug", "_noop"])
        assert result.exit_code == 0
        assert "ran" in result.output
    finally:
        dtool.commands.pop("_noop", None)


def test_version_option_reports_components():
    from dtool_cli.cli import dtool
    runner = CliRunner()
    result = runner.invoke(dtool, ["--version"])
    assert result.exit_code == 0
    assert "dtoolcore, version" in result.output
    assert "dtool-cli, version" in result.output


def test_pretty_version_text_is_string():
    from dtool_cli.cli import pretty_version_text
    text = pretty_version_text()
    assert isinstance(text, str)
    assert "Storage brokers:" in text
    assert "Plugins:" in text


def test_iter_entry_points_returns_iterable():
    # The wrapper bridges the importlib.metadata group= API across versions;
    # an unknown group should yield an empty (but iterable) result.
    from dtool_cli.cli import iter_entry_points
    assert list(iter_entry_points("dtool.no_such_group")) == []
