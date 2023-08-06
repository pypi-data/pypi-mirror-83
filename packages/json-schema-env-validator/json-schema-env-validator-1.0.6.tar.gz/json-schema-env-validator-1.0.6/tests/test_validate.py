import os

import jsonschema
import pytest

import enviral


def test_validate_from_env(env):
    os.environ["FOO"] = "bar"
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string"}, "bar": {"type": "string"}},
        "required": ["foo", "bar"],
    }
    with pytest.raises(jsonschema.exceptions.ValidationError):
        enviral.validate_env(schema)

    os.environ["BAR"] = "foo"
    enviral.validate_env(schema)


def test_validate_number_from_env(env):
    os.environ["FOO"] = "bar"
    schema = {"type": "object", "properties": {"foo": {"type": "number"}}}
    with pytest.raises(jsonschema.exceptions.ValidationError):
        enviral.validate_env(schema)

    # Check int
    os.environ["FOO"] = "2"
    settings = enviral.validate_env(schema)
    assert settings["foo"] == 2

    # Check float
    os.environ["FOO"] = "2.25"
    settings = enviral.validate_env(schema)
    assert settings["foo"] == 2.25


def test_validate_integer_from_env(env):
    os.environ["FOO"] = "bar"
    schema = {"type": "object", "properties": {"foo": {"type": "integer"}}}
    with pytest.raises(jsonschema.exceptions.ValidationError):
        enviral.validate_env(schema)

    # Check int
    os.environ["FOO"] = "50"
    settings = enviral.validate_env(schema)
    assert settings["foo"] == 50

    # Float should fail
    os.environ["FOO"] = "2.25"
    with pytest.raises(jsonschema.exceptions.ValidationError):
        enviral.validate_env(schema)
