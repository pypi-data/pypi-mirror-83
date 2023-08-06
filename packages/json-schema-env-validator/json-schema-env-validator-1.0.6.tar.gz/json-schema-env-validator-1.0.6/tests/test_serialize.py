import enviral
import os


def test_get_setting_from_env(env):
    os.environ["FOO"] = "bar"
    settings = enviral.serialize(
        {"type": "object", "properties": {"foo": {"type": "string"}}}
    )
    assert "FOO" not in settings
    assert "foo" in settings
    assert settings["foo"] == "bar"


def test_get_setting_from_env_with_prefix(env):
    os.environ["PREFIX_FOO"] = "bar"
    settings = enviral.serialize(
        {"type": "object", "properties": {"foo": {"type": "string"}}}, prefix="PREFIX_"
    )
    assert "FOO" not in settings
    assert "foo" in settings
    assert settings["foo"] == "bar"



def test_convert_number_setting_from_env(env):
    for number, conversion in (("2", int), ("9.85", float)):
        os.environ["FOO"] = number
        settings = enviral.serialize(
            {"type": "object", "properties": {"foo": {"type": "number"}}}
        )
        assert settings["foo"] == conversion(number)


def test_convert_int_setting_from_env(env):
    os.environ["FOO"] = "250"
    settings = enviral.serialize(
        {"type": "object", "properties": {"foo": {"type": "integer"}}}
    )
    assert settings["foo"] == 250


def test_convert_object_setting_from_env(env):
    os.environ["FOO"] = '{"foo": "bar"}'
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {
                "foo": {"type": "object", "properties": {"foo": {"type": "string"}}}
            },
        }
    )
    assert settings["foo"] == {"foo": "bar"}


def test_convert_list_setting_from_env(env):
    os.environ["FOO"] = '["foo", "bar"]'
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {"foo": {"type": "array", "items": {"type": "string"}}},
        }
    )
    assert settings["foo"] == ["foo", "bar"]


def test_convert_bool_setting_from_env(env):
    for setting in ("1", "true", "TRUE", "y", "YES"):
        os.environ["FOO"] = setting
        settings = enviral.serialize(
            {"type": "object", "properties": {"foo": {"type": "boolean"}}}
        )
        assert settings["foo"] is True

    for setting in ("0", "false", "FALSE", "n", "no"):
        os.environ["FOO"] = setting
        settings = enviral.serialize(
            {"type": "object", "properties": {"foo": {"type": "boolean"}}}
        )
        assert settings["foo"] is False


def test_get_json_from_module_file(env):
    os.environ["FOOBAR"] = "bar"
    settings = enviral.serialize("enviral:test-env-schema.json")
    assert settings["foobar"] == "bar"


def test_fill_default_json_schema_value(env):
    os.environ["FOO"] = "bar"
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {
                "foo": {"type": "string"},
                "bar": {"type": "string", "default": "foo"},
            },
        }
    )
    assert settings == {"foo": "bar", "bar": "foo"}


def test_get_env_case_insensitive(env):
    os.environ["FOO"] = "Bar"
    assert enviral.get_env("foo") == "Bar"
    assert enviral.get_env("Foo") == "Bar"
    assert enviral.get_env("FOO") == "Bar"


def test_array_from_comma_values(env):
    os.environ["FOO"] = "foo,bar"
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {"foo": {"type": "array", "items": {"type": "string"}}},
        }
    )
    assert settings == {"foo": ["foo", "bar"]}


def test_array_from_comma_single_value(env):
    os.environ["FOO"] = "foo"
    settings = enviral.serialize(
        {
            "type": "object",
            "properties": {"foo": {"type": "array", "items": {"type": "string"}}},
        }
    )
    assert settings == {"foo": ["foo"]}
