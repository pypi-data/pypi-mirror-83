# @Time   : 2020-04-24
# @Author : zhangxinhao
import cv2
from .cap_template import CapTemplate
import typing
class DefaultCap(CapTemplate):
    @staticmethod
    def _make_handles(device_name, cap, args, fps, resize_flag, in_width, in_height, out_width, out_height) -> typing.Any:
        resizer = None
        if resize_flag:
            resizer = lambda x: cv2.resize(x, (out_width, out_height))
        return {
            "cap": cap,
            "resizer": resizer,
            "resize_flag": resize_flag,
        }


    @staticmethod
    def _open(device_name, args):
        if device_name.isdigit():
            device_name = int(device_name)
        cap = cv2.VideoCapture(device_name)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if (fps > 100) or (fps < 1):
            fps = 25
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width =  cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        return cap, width, height, fps

    @staticmethod
    def _grab(handlers) -> typing.Any:
        return handlers['cap'].grab()

    @staticmethod
    def _retrieve(grab_cache, handlers):
        ret, img = handlers['cap'].retrieve()
        if ret:
            if handlers['resize_flag']:
                img = handlers['resizer'](img)
            return img

