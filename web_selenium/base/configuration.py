import json
import os
from configparser import ConfigParser
import yaml


def _load_ini_file(ini_file):
    instance_ini = ConfigParser()
    try:
        instance_ini.read(ini_file, encoding='utf-8')
    except Exception as error:
        err_msg = f"IniError:\nfile: {ini_file}\nerror: {error}"
        raise error

    # self.config.items(section) 返回内容指定部分
    # 返回所有内容
    return instance_ini.sections()


def _load_json_file(json_file):
    """
    获取json文件内容
    :param json_file:
    :return:
    """
    with open(json_file, encoding="utf-8") as data_path:
        try:
            json_content = json.load(data_path)
            print(json_content)
        except json.JSONDecodeError as error:
            err_msg = f"JsonError:\nfile: {json_file}\nerror: {error}"
            raise err_msg
        return json_content

def _load_yaml_file(yaml_file):
    """
    根据路径获取yaml文件内容
    :param path:
    :return:
    """
    with open(yaml_file, encoding='utf-8') as casepath:
        try:
            yaml_content = yaml.safe_load(casepath)
            print(yaml_content)
        except yaml.YAMLError as error:
            err_msg = f"YamlError:\nfile: {yaml_file}\nerror: {error}"
            raise err_msg

    return yaml_content


def load_file(load_file, load_type='ini'):
    # 传入路径与模式，加载文件内容
    if not os.path.isfile(load_file):
        raise FileNotFoundError(f"load_file not exists: {load_file}")

    if "ini" in load_type:
        file_content = _load_ini_file(load_file)
    elif "yaml" in load_type or "yml" in load_type:
        file_content = _load_yaml_file(load_file)
    elif "json" in load_type:
        file_content = _load_json_file(load_file)
    else:
        raise("Load File Type should be 'option'、'test' or 'json' ")
    return file_content

