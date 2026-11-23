"""Tests for the reusable click argument validation callbacks."""

import pytest

import click

import dtoolcore

from dtool_cli.cli import (
    storagebroker_validation,
    base_dataset_uri_validation,
    proto_dataset_uri_validation,
    dataset_uri_validation,
)


@pytest.fixture
def datasets(tmp_path):
    """Create a proto and a frozen dataset in a temporary file base URI.

    Returns a dict with the ``base``, ``proto`` and ``frozen`` URIs.
    """
    base_uri = "file://{}".format(tmp_path)

    proto = dtoolcore.create_proto_dataset("proto_ds", base_uri)

    frozen = dtoolcore.create_proto_dataset("frozen_ds", base_uri)
    frozen.freeze()

    return {"base": base_uri, "proto": proto.uri, "frozen": frozen.uri}


def test_storagebroker_validation_accepts_known_broker():
    assert storagebroker_validation(None, None, "file") == "file"


def test_storagebroker_validation_rejects_unknown_broker():
    with pytest.raises(click.BadParameter):
        storagebroker_validation(None, None, "no-such-broker")


def test_base_dataset_uri_validation_accepts_dataset(datasets):
    uri = datasets["proto"]
    assert base_dataset_uri_validation(None, None, uri) == uri


def test_base_dataset_uri_validation_rejects_non_dataset(datasets):
    with pytest.raises(click.BadParameter):
        base_dataset_uri_validation(None, None, datasets["base"])


def test_proto_dataset_uri_validation_accepts_proto(datasets):
    uri = datasets["proto"]
    assert proto_dataset_uri_validation(None, None, uri) == uri


def test_proto_dataset_uri_validation_rejects_frozen(datasets):
    with pytest.raises(click.BadParameter):
        proto_dataset_uri_validation(None, None, datasets["frozen"])


def test_dataset_uri_validation_accepts_frozen(datasets):
    uri = datasets["frozen"]
    assert dataset_uri_validation(None, None, uri) == uri


def test_dataset_uri_validation_rejects_proto(datasets):
    with pytest.raises(click.BadParameter):
        dataset_uri_validation(None, None, datasets["proto"])
