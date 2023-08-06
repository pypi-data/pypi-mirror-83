# @Time   : 2020-04-24
# @Author : zhangxinhao
from aixm.contrib.vpf.nv_codec import *
from .cap_template import CapTemplate
import numpy as np
import typing
class NviCap(CapTemplate):
    @staticmethod
    def _make_handles(device_name, cap, args, fps, resize_flag, in_width, in_height, out_width, out_height) -> typing.Any:
        gpu_id = args[0]
        converter = SurfaceConverter(in_width, in_height,
                                          PixelFormat.NV12, PixelFormat.BGR, gpu_id)
        downloader = SurfaceDownloader(out_width, out_height, PixelFormat.BGR, gpu_id)
        resizer = None
        if resize_flag:
            resizer = SurfaceResizer(out_width, out_height, PixelFormat.BGR, gpu_id)
        reshaper = lambda x: np.reshape(x, (out_height, out_width, 3))
        return {
            "cap": cap,
            "converter": converter,
            "resizer": resizer,
            "resize_flag": resize_flag,
            "downloader": downloader,
            "reshaper": reshaper
        }

    @staticmethod
    def _open(device_name, args):
        gpu_id = args[0]
        nv_decode = NvDecoder(device_name, gpu_id)
        fps = nv_decode.Framerate()
        if (fps > 100) or (fps < 1):
            fps = 25
        return nv_decode, nv_decode.Width(), nv_decode.Height(), fps

    @staticmethod
    def _grab(handlers) -> typing.Any:
        return handlers['cap'].DecodeSingleSurface()

    @staticmethod
    def _retrieve(grab_cache, handlers):
        if (grab_cache.Empty()):
            return
        sf_bgr= handlers['converter'].Execute(grab_cache)
        if (sf_bgr.Empty()):
            return
        if handlers['resize_flag']:
            sf_bgr = handlers['resizer'].Execute(sf_bgr)
        np_bgr = handlers['downloader'].DownloadSingleSurface(sf_bgr)
        if not (np_bgr.size):
            return
        return handlers['reshaper'](np_bgr)
