# @Time   : 2019-01-29
# @Author : zhangxinhao
if False:
    import typing
    import logging


    # convert ...........................................................................
    def to_jsonlist(l) -> None:
        pass

    def to_jsondict(d) -> None:
        pass

    def to_abstract_jsonlist(l) -> list:
        pass

    def to_abstract_jsondict(d) -> dict:
        pass


    # dsop ..............................................................................
    def get_dict_from_dict(obj, key) -> dict:
        pass

    def get_list_from_dict(obj, key) -> list:
        pass

    def get_any_from_dict(obj, key, creator) -> typing.Any:
        pass

    class CircularQueue:
        def __init__(self, size):
            pass
        def put(self, data):
            pass
        def __getitem__(self, index) -> typing.Any:
            pass
        def __iter__(self):
            pass
        def getall(self) -> list:
            pass

    # lock ..............................................................................
    def lock_class_func(instance, func, mutex_name='', timeout=3) -> None:
        pass

    def lock_func(mutex=None, timeout=3) -> typing.Any:
        pass


    # logging ...........................................................................
    def set_logid(log_id) -> None:
        pass

    def init_logger(appname=None, filename=None, log_id=None, exist_ok=False,
                open_console=True, open_localfile=True, open_collect=False, level='DEBUG',
                rotating_conf={'when':'W0','interval':1,'backupCount':53},
                collect_address=('localhost', 6666)) -> None:
        pass

    def log() -> logging.Logger:
        pass


    # logging_server ....................................................................
    def start_logging_server(host='0.0.0.0', port=6666) -> None:
        pass


    # path ..............................................................................
    def search_filepaths(root_path, file_filter) -> list:
        pass

    def parse_filepath_prefix(filepath) -> str:
        pass

    def parse_filepath_suffix(filepath) -> str:
        pass

    def parse_filepath_name(filepath) -> str:
        pass

    def parse_filepath_parent_name(filepath) -> str:
        pass

    def parse_filepath_dir(filepath) -> str:
        pass

    def replace_filepath_suffix(filepath, new_suffix) -> str:
        pass

    def split_filepath(filepath) -> str:
        pass

    # strategy ..........................................................................
    class RecordByTime:
        def __init__(self, sec, num):
            pass
        def set(self) -> bool:
            pass
        def get(self) -> bool:
            pass
        def clear(self) -> None:
            pass

    class RecordByFrequency:
        def __init__(self, size, mean_over):
            pass
        def set(self, n) -> bool:
            pass
        def get(self) -> bool:
            pass
        def clear(self) -> None:
            pass


    # utils .............................................................................
    def cal_str_md5(s) -> str:
        pass

    def cal_file_md5(filepath) -> str:
        pass

    def remove_file(filepath) -> None:
        pass

    def encrypt(src_file, dest_file, secret_key, block_size=16):
        pass

    def decrypt(src_file, dest_file, secret_key, block_size=16):
        pass

    def current_time() -> tuple:
        pass

    def is_x86() -> bool:
        pass


    class TimeNow:

        def timestamp(self) -> float:
            pass

        def ymd(self) -> str:
            pass

        def hms(self) -> str:
            pass

        def ymdhms(self) -> str:
            pass

        def ymdhms_strip(self) -> str:
            pass

        def ymdhmsm(self) -> str:
            pass

        def ymdhmsm_strip(self) -> str:
            pass

    # working ...........................................................................
    def kill_other(name, key=None, is_create_new=True) -> None:
        pass

    def kill_all(key) -> None:
        pass

    def run_this(name, *args, **kwargs) -> typing.Any:
        pass

    def get_class_or_func(class_or_func_path) -> typing.Any:
        pass

    def collect_modules(root_path, root_package) -> list:
        pass

    def find_attributes(root_path, root_package, class_filter) -> list:
        pass


    # ztimer ............................................................................
    class ZTimer:
        def __init__(self, task_info):
            self.task_info = task_info
            self.interval = 0.001
            if task_info.get('interval') is not None:
                self.interval = task_info.get('interval')
        def init(self):
            pass
        def init_run(self):
            pass
        def do(self):
            pass
        def run(self):
            pass

    def timer_add_task(task_info) -> None:
        pass

    def timer_start_all() -> None:
        pass

    def timer_stop_all() -> None:
        pass

from aixm._internal.path import *
from .logging import *
from .logging_server import *
from .convert import *
from .lock import *
from .path import *
from .strategy import *
from .utils import *
from .dsop import *
from .working import *
from .ztimer import *