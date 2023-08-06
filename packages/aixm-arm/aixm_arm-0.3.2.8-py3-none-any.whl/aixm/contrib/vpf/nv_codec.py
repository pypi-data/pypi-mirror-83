# @Time   : 2020-04-22
# @Author : zhangxinhao
from aixm.utils import relative_project_path as _relative_project_path
import sys as _sys

_sys.path.append(_relative_project_path('lib'))
import importlib as _importlib

_nvc = _importlib.import_module('PyNvCodec')
PixelFormat = _nvc.PixelFormat
SurfacePlane = _nvc.SurfacePlane
Surface = _nvc.Surface
NvEncoder = _nvc.PyNvEncoder
NvDecoder = _nvc.PyNvDecoder
FrameUploader = _nvc.PyFrameUploader
SurfaceDownloader = _nvc.PySurfaceDownloader
SurfaceConverter = _nvc.PySurfaceConverter
SurfaceResizer = _nvc.PySurfaceResizer
GetNumGpus = _nvc.GetNumGpus

if False:
    import numpy as np
    class PixelFormat:
        Y = 0
        RGB = 0
        NV12 = 0
        YUV420 = 0
        RGB_PLANAR = 0
        UNDEFINED = 0
        BGR = 0


    class SurfacePlane:
        def Width(self) -> int:
            pass

        def Height(self) -> int:
            pass

        def Pitch(self) -> int:
            pass

        def GpuMem(self) -> int:
            pass

        def ElemSize(self) -> int:
            pass


    class Surface:
        def Width(self) -> int:
            pass

        def Height(self) -> int:
            pass

        def Pitch(self) -> int:
            pass

        def PixelFormat(self) -> int:
            pass

        def Empty(self) -> bool:
            pass

        def NumPlanes(self) -> int:
            pass

        @staticmethod
        def Make(pixel_format, new_width, new_height):
            return Surface()

        def PlanePtr(self) -> SurfacePlane:
            pass

        def CopyFrom(self, other_surface, gpu_id) -> None:
            pass

        def Clone(self, gpu_id):
            return Surface()


    class NvEncoder:
        def __init__(self, encode_opt, gpu_id):
            pass

        def Width(self) -> int:
            pass

        def Height(self) -> int:
            pass

        def PixelFormat(self) -> int:
            pass

        def EncodeSingleSurface(self) -> np.ndarray:
            pass

        def EncodeSingleFrame(self) -> np.ndarray:
            pass

        def Flush(self) -> list:
            pass


    class NvDecoder:
        def __init__(self, device, gpu_id):
            pass

        def Width(self) -> int:
            pass

        def Height(self) -> int:
            pass

        def Framerate(self) -> int:
            pass

        def PixelFormat(self) -> int:
            pass

        def DecodeSingleSurface(self) -> Surface:
            pass

        def DecodeSingleFrame(self) -> np.ndarray:
            # flatten
            pass


    class FrameUploader:
        def __init__(self, width, height, format, gpu_id):
            pass

        def UploadSingleFrame(self, frame) -> Surface:
            pass


    class SurfaceDownloader:
        def __init__(self, width, height, format, gpu_id):
            pass

        def DownloadSingleSurface(self, surface) -> np.ndarray:
            pass


    class SurfaceConverter:
        def __init__(self, width, height, in_format, out_format, gpu_id):
            pass

        def Execute(self, surface) -> Surface:
            pass


    class SurfaceResizer:
        def __init__(self, width, height, format, gpu_id):
            pass

        def Execute(self, surface) -> Surface:
            pass


    def GetNumGpus() -> int:
        pass
