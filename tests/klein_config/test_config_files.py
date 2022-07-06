# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import pytest
import argparse
import os

yamlString = """
key: value
level1:
  level2:
    key: value
"""

jsonString = """
{
    "key":"value",
    "level1": {
        "level2": {
            "key": "value"
        }
    }
}
"""

hoconString = '''
{
    key = value
    level1 {
        level2 = {
            key: ${key}
        }
    }
    altkey = substituted ${key}
}
'''


class TestConfigWithFilesWithArgs:

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.yml", common=None), argparse.Namespace()))
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=yamlString)
    def test_with_yaml_file(self, mock_open, mock_args):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.yml', 'r')
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("level1.level2.key") == "value"
        assert config["level1.level2.key"] == "value"
        nested = config["level1"]
        assert nested["level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.json", common=None), argparse.Namespace()))
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=jsonString)
    def test_with_json_file(self, mock_open, mock_args):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.json', 'r')
        assert config.get("key") == "value"
        assert config.get("level1.level2.key") == "value"
        assert config["key"] == "value"
        assert config["level1.level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.conf", common=None), argparse.Namespace()))
    @mock.patch('codecs.open', new_callable=mock.mock_open, read_data=hoconString)
    def test_with_hocon_file(self, mock_open, mock_args):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.conf', 'r', encoding="utf-8")
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("altkey") == "substituted value"
        assert config["altkey"] == "substituted value"
        assert config.get("level1.level2.key") == "value"
        assert config["level1.level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.conf", common="dummy2.conf"), argparse.Namespace()))
    @mock.patch('codecs.open', new_callable=mock.mock_open, read_data=hoconString)
    def test_with_hocon_files_config_and_common(self, mock_open, mock_args):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_any_call('dummy2.conf', 'r', encoding="utf-8")
        mock_open.assert_any_call('dummy.conf', 'r', encoding="utf-8")
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("altkey") == "substituted value"
        assert config["altkey"] == "substituted value"
        assert config.get("level1.level2.key") == "value"
        assert config["level1.level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch.dict(os.environ, {'LEVEL1_LEVEL2_KEY': 'env_value'})
    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.yml", common=None), argparse.Namespace()))
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=yamlString)
    def test_nested_env_with_yaml_file(self, mock_open, mock_args):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.yml', 'r')
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("level1.level2.key") == "env_value"
        assert config["level1.level2.key"] == "env_value"
        nested = config["level1"]
        assert nested["level2.key"] == "env_value"
        assert config["level1"]["level2"]["key"] == "env_value"


class TestConfigWithFilesWithEnvironmentalVariable:

    @mock.patch.dict(os.environ, {'PY_ENV_AWARE_CONFIG': 'dummy.yml'})
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=yamlString)
    def test_with_yaml_file(self, mock_open):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.yml', 'r')
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("level1.level2.key") == "value"
        assert config["level1.level2.key"] == "value"
        nested = config["level1"]
        assert nested["level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch.dict(os.environ, {'PY_ENV_AWARE_CONFIG': 'dummy.json'})
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=jsonString)
    def test_with_json_file(self, mock_open):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.json', 'r')
        assert config.get("key") == "value"
        assert config.get("level1.level2.key") == "value"
        assert config["key"] == "value"
        assert config["level1.level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch.dict(os.environ, {'PY_ENV_AWARE_CONFIG': 'dummy.conf'})
    @mock.patch('codecs.open', new_callable=mock.mock_open, read_data=hoconString)
    def test_with_hocon_file(self, mock_open):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.conf', 'r', encoding="utf-8")
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("altkey") == "substituted value"
        assert config["altkey"] == "substituted value"
        assert config.get("level1.level2.key") == "value"
        assert config["level1.level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch.dict(os.environ, {'KLEIN_CONFIG': 'dummy.conf', 'KLEIN_COMMON': 'dummy2.conf'})
    @mock.patch('codecs.open', new_callable=mock.mock_open, read_data=hoconString)
    def test_with_hocon_files_config_and_common(self, mock_open):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_any_call('dummy2.conf', 'r', encoding="utf-8")
        mock_open.assert_any_call('dummy.conf', 'r', encoding="utf-8")
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("altkey") == "substituted value"
        assert config["altkey"] == "substituted value"
        assert config.get("level1.level2.key") == "value"
        assert config["level1.level2.key"] == "value"
        assert config["level1"]["level2"]["key"] == "value"

    @mock.patch.dict(os.environ, {'LEVEL1_LEVEL2_KEY': 'env_value', 'PY_ENV_AWARE_CONFIG': 'dummy.yml'})
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=yamlString)
    def test_nested_env_with_yaml_file(self, mock_open):
        from src.klein_config.config import get_config
        config = get_config()
        mock_open.assert_called_with('dummy.yml', 'r')
        assert config.get("key") == "value"
        assert config["key"] == "value"
        assert config.get("level1.level2.key") == "env_value"
        assert config["level1.level2.key"] == "env_value"
        nested = config["level1"]
        assert nested["level2.key"] == "env_value"
        assert config["level1"]["level2"]["key"] == "env_value"


class TestConfigwithFilesInvalid:

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.yml", common=None), argparse.Namespace()))
    @mock.patch.dict(os.environ, {'PY_ENV_AWARE_CONFIG': 'dummy.yml'})
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=yamlString)
    def test_with_both_arg_and_env(self, mock_open, mock_args):
        from src.klein_config.config import get_config
        with pytest.raises(Exception):
            config = get_config()
