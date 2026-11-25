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


def test_version_text_not_built_unless_requested(mocker):
    # Building the version text imports every plugin; it must not happen on
    # import or for other invocations such as --help.
    from dtool_cli.cli import dtool
    pretty = mocker.patch("dtool_cli.cli.pretty_version_text",
                          return_value="VERSION TEXT")
    runner = CliRunner()

    result = runner.invoke(dtool, ["--help"])
    assert result.exit_code == 0
    pretty.assert_not_called()

    result = runner.invoke(dtool, ["--version"])
    assert result.exit_code == 0
    assert result.output == "VERSION TEXT\n"
    pretty.assert_called_once_with()


def test_pretty_version_text_tolerates_broken_plugins(mocker):
    from types import SimpleNamespace
    from dtool_cli.cli import pretty_version_text

    def broken_load():
        raise ImportError("broken storage broker")

    entry_points = {
        # "os" exists but has no __version__; "no_such_pkg" cannot be imported.
        "dtool.storage_brokers": [
            SimpleNamespace(name="BrokenBroker", module="no_such_pkg.broker",
                            load=broken_load),
        ],
        "dtool.cli": [
            SimpleNamespace(name="noversion", module="os"),
        ],
    }
    mocker.patch("dtool_cli.cli.iter_entry_points",
                 side_effect=lambda group: entry_points.get(group, []))

    text = pretty_version_text()
    assert "BrokenBroker, no-such-pkg, version unknown" in text
    assert "os, version unknown" in text


def _with_failing_command(args, error):
    import click
    from dtool_cli.cli import dtool

    @dtool.command(name="_fail")
    @click.argument("uri", required=False)
    def _fail(uri):
        raise error

    try:
        return CliRunner().invoke(dtool, args)
    finally:
        dtool.commands.pop("_fail", None)


def test_errors_reported_without_traceback():
    """Errors of storage brokers are reported in one line, exit code 1."""
    result = _with_failing_command(
        ["_fail"], RuntimeError("Not logged in to dserver example.org"))
    assert result.exit_code == 1
    assert "Error: Not logged in to dserver example.org" in result.output
    assert "dtool --debug" in result.output
    assert "Traceback" not in result.output


def test_errors_with_traceback_in_debug_mode():
    error = RuntimeError("broken")
    result = _with_failing_command(["--debug", "_fail"], error)
    assert result.exit_code == 1
    assert result.exception is error


def test_errors_of_parameter_callbacks_reported(tmp_path):
    """Validating a dataset URI contacts storage, which can fail."""
    import click
    from dtool_cli.cli import dtool

    def callback(ctx, param, value):
        raise ValueError(f"Invalid URI: {value}")

    @dtool.command(name="_fail")
    @click.argument("uri", callback=callback)
    def _fail(uri):
        pass

    try:
        result = CliRunner().invoke(dtool, ["_fail", "nope://x"])
    finally:
        dtool.commands.pop("_fail", None)
    assert result.exit_code == 1
    assert "Error: Invalid URI: nope://x" in result.output


def test_click_errors_unchanged():
    import click
    result = _with_failing_command(["_fail"], click.UsageError("bad usage"))
    assert result.exit_code == 2
    assert "bad usage" in result.output
    assert "dtool --debug" not in result.output
