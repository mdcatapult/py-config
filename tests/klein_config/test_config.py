import os
import mock
import pytest
from src.klein_config.config import EnvironmentAwareConfig
from pyhocon.exceptions import ConfigMissingException

initial_config = dict()
initial_config["key"] = "value"
initial_config["level1"] = dict()
initial_config["level1"]["level2"] = dict()
initial_config["level1"]["level2"]["key"] = "value"
config = EnvironmentAwareConfig(initial_config)


@mock.patch.dict(os.environ, {'ENV_KEY': 'env_value'})
def test_for_valid_environment_key_with_dot_notation():
    assert config.get("env.key") == "env_value"
    assert config["env.key"] == "env_value"


def test_for_invalid_key():
    with pytest.raises(ConfigMissingException):
        config.get("bad.key")
    with pytest.raises(KeyError):
        config["bad.key"]


def test_for_valid_nested_config_level():
    assert config.get("level1.level2.key") == "value"
    assert config["level1.level2.key"] == "value"


def test_for_valid_has():
    assert config.has("level1.level2.key")


def test_for_invalid_has():
    assert not config.has("bad.key")


def test_for_invalid_has_no_initial_state():
    empty_config = EnvironmentAwareConfig()
    assert not empty_config.has("bad.key.no.init")


def test_for_default_value_on_invalid_key():
    assert config.get("bad.key", "default") == "default"
