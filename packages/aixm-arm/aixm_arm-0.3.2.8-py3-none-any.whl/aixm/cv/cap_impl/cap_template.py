# @Time   : 2020-04-24
# @Author : zhangxinhao
import numpy as np
import typing
from aixm.utils import log
import traceback

class CapTemplate:
    '''
    实现四个静态方法
    '''
    def __init__(self, device_name, out_width=None, out_height=None, args=()):
        self._device_name = device_name # type: str
        self._args = args
        self._open_flag = False
        self.open()
        self._resize_flag = True
        if (out_width is None) or (out_height is None):
            self._resize_flag = False
            self._out_width = self._in_width
            self._out_height = self._in_height
        else:
            self._out_width = out_width
            self._out_height = out_height
        self._handlers = self._make_handles(self._device_name, self._cap, self._args, self._fps, self._resize_flag,
                                            self._in_width, self._in_height, self._out_width, self._out_height)

        self._grab_cache = None

    def file_or_stream(self) -> str:
        if self._device_name.startswith('rtsp') or self._device_name.isdigit():
            return "stream"
        return 'file'

    def open(self):
        if self._open_flag:
            return
        else:
            self._cap, self._in_width, self._in_height, self._fps = self._open(self._device_name, self._args)
            self._open_flag = True

    def close(self):
        if self._open_flag:
            self._close(self._cap)
            self._cap = None
            self._open_flag = False

    def reopen(self):
        self.close()
        self.open()

    def is_open(self) -> bool:
        return self._open_flag

    def width(self) -> int:
        return self._out_width

    def height(self) -> int:
        return self._out_height

    def fps(self) -> int:
        return self._fps

    def read(self) -> np.ndarray:# or None
        self.grab()
        return self.retrieve()

    def grab(self):
        try:
            self._grab_cache = self._grab(self._handlers)
        except:
            log().error("device: %s, grab error" % self._device_name)
            log().error(traceback.format_exc(200))

    def retrieve(self) -> np.ndarray:# or None
        try:
            return self._retrieve(self._grab_cache, self._handlers)
        except:
            log().error("device: %s, retrieve error" % self._device_name)
            log().error(traceback.format_exc(200))

    @staticmethod
    def _make_handles(device_name, cap, args, fps, resize_flag, in_width, in_height, out_width, out_height) -> typing.Any:
        '''
        返回即为_grab,_retrieve的传入参数
        '''
        pass

    @staticmethod
    def _open(device_name, args)-> tuple:
        '''
        Return cap, width, height, fps
        '''
        pass

    @staticmethod
    def _close(cap):
        pass

    @staticmethod
    def _grab(handlers) -> typing.Any:
        pass

    @staticmethod
    def _retrieve(grab_cache, handlers) -> np.ndarray:# or None
        pass
