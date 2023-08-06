# coding: utf-8
import yaml
import os


def get_yaml_data(yaml_file):
    '''
    :param yaml_file:
    :return:返回同名object文件，共用object文件加REP
    '''
    current_path = os.path.abspath('.')
    yaml_path = os.path.join(current_path, yaml_file) + '.yaml'

    fe = os.path.exists(yaml_path)
    if not fe:
        yaml_file = yaml_file.replace('REP', '')
        yaml_path = os.path.join(current_path, yaml_file) + '.yaml'

    file = open(yaml_path, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    data = yaml.safe_load(file_data)

    return data
