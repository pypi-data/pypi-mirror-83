# @Time   : 2020-04-02
# @Author : zhangxinhao
import os
import sys
import json

class __path_object:
    pass

def __init_path():
    project_path = os.getenv('PROJECTPATH')
    if project_path is None:
        file_path = os.path.realpath(sys.argv[0])
        index = file_path.find('/src/')
        if index == -1:
            print('PROJECTPATH, src 目录不存在!')
            sys.exit(0)
        project_path = file_path[:index]
    sys.path.append(os.path.join(project_path, 'src'))
    __path_object.project_path = project_path
    __path_object.data_path = os.path.join(project_path, 'data')
    __path_object.models_path = os.path.join(project_path, 'models')
    __path_object.conf_path = os.path.join(project_path, 'conf')
    __path_object.logs_path = os.path.join(project_path, 'logs')

    _splits = project_path.split('/')
    _project_name = _splits[-1]
    _splits.pop(-1)
    if _splits[0] == '':
        _splits.pop(0)
    _project_hash = '.'.join(map(lambda x: x[:3], _splits)) + '.' + _project_name

    def replace_hash(path):
        return path.replace('<project_hash>', _project_hash)

    config_path = None
    if os.path.isfile(os.path.expanduser('~/.config/aixm_config.json')):
        config_path = os.path.expanduser('~/.config/aixm_config.json')
    if os.path.isfile(os.path.join(project_path, 'aixm_config.json')):
        config_path = os.path.join(project_path, 'aixm_config.json')

    if config_path is not None:
        with open(config_path) as f:
            path_dict = json.load(f)

            data_path = path_dict.get('data_path')
            if data_path is not None:
                __path_object.data_path = replace_hash(data_path)

            models_path = path_dict.get('models_path')
            if models_path is not None:
                __path_object.models_path = replace_hash(models_path)

            conf_path = path_dict.get('conf_path')
            if conf_path is not None:
                __path_object.conf_path = replace_hash(conf_path)

            logs_path = path_dict.get('logs_path')
            if logs_path is not None:
                __path_object.logs_path = replace_hash(logs_path)

    print('PROJECT_PATH=' + __path_object.project_path)
    print('DATA_PATH=' + __path_object.data_path)
    print('MODELS_PATH=' + __path_object.models_path)
    print('CONF_PATH=' + __path_object.conf_path)
    print('LOGS_PATH=' + __path_object.logs_path)
    print('*' * 36)


__init_path()

def reset_path():
    project_path = __path_object.project_path
    __path_object.data_path = os.path.join(project_path, 'data')
    __path_object.models_path = os.path.join(project_path, 'models')
    __path_object.conf_path = os.path.join(project_path, 'conf')
    __path_object.logs_path = os.path.join(project_path, 'logs')


def relative_project_path(*args):
    return os.path.realpath(os.path.join(__path_object.project_path, *args))


def relative_data_path(*args):
    return os.path.realpath(os.path.join(__path_object.data_path, *args))


def relative_conf_path(*args):
    return os.path.realpath(os.path.join(__path_object.conf_path, *args))


def relative_models_path(*args):
    return os.path.realpath(os.path.join(__path_object.models_path, *args))


def relative_logs_path(*args):
    return os.path.realpath(os.path.join(__path_object.logs_path, *args))


_config_dict = dict()

def local_config(config_name='config.json'):
    config = _config_dict.get(config_name)
    if config is None:
        with open(relative_conf_path(config_name)) as f:
            config = json.load(f)
            _config_dict[config_name] = config
    if config is None:
        raise Exception('config.json is not exist!')
    return config


def set_local_config(config_name, config):
    _config_dict[config_name] = config


__all__ = ['reset_path',
           'relative_project_path',
           'relative_data_path',
           'relative_conf_path',
           'relative_models_path',
           'relative_logs_path',
           'local_config',
           'set_local_config']
