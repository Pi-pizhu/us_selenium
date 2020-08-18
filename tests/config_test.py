import json
import re

from jsonpath import jsonpath

from web_selenium.base.configuration import *
from web_selenium.base.sys_operation import *


def assert_for(list_data, pattern):
    if isinstance(list_data, list):
        for data in list_data:
            assert not re.search(pattern, data)


class TestConfig:
    
    _path = '/Users/yewenkai/PycharmProjects/us_selenium/tests/data'

    # def test_ini_file(self):
    #     files = configuration.ReadIni.get_ini_file(self._path)
    #     assert_for(files, r'\.[^in]')

    def test_ini_content(self):
        ini_file = 'config.ini'
        ini_path = join_path(self._path, ini_file)
        init_content = load_file(ini_path)
        print(init_content)

    # def test_ini_read(self):
    #     files = configuration.ReadIni.get_ini_file(self._path)
    #     ini_path = sys_operation.join_path(self._path, files[0])
    #     ini_instance = configuration.ReadIni(ini_path)
    #     sections = ini_instance.get_list_section()
    #     config = ini_instance.specified_section(sections[1])
    #     assert isinstance(config, list)
    #     assert config[0] == ('chrome_browser', '/User/yewenkai/Public/Chrome/chromedriver.exe')

    # def test_yaml_file(self):
    #     files = configuration.ReadYaml.get_all_documents(self._path)
    #     assert_for(files, r'\.[^yaml]')

    def test_yaml_content(self):
        yml_file = 'firefox_test_steps.yaml'
        yml_path = join_path(self._path, yml_file)
        yml_content = load_file(yml_path, 'yml')
        print(yml_content)
        # assert yml_data.get('url')
        # assert isinstance(yml_data.get('teststep'), dict)
        # teststep = jsonpath(yml_data, '$..test_step')[0]
        # assert teststep.get('steps_path')
        # assert teststep.get('action')
        # assert teststep.get('input')

    def test_json_content(self):
        json_file = 'browser_options.json'
        json_path = join_path(self._path, json_file)
        json_content = load_file(json_path, 'json')
        print(json_content)
        print(type(json_content))