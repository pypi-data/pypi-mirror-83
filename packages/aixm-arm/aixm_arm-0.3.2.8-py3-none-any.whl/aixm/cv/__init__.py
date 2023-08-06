# @Time   : 2018-11-16
# @Author : zhangxinhao
if False:
    import numpy as np
    import typing
    import threading
    import cv2

    # box
    class Box_:
        def __init__(self, top, left, height, width):
            self.top = 0
            self.left = 0
            self.height = 0
            self.width = 0
            self.bottom = 0
            self.right = 0

        def to_tlhw(self) -> tuple:
            pass

        def to_ltwh(self) -> tuple:
            pass

        def to_tlbr(self) -> tuple:
            pass

        def to_ltrb(self) -> tuple:
            pass

        def area(self) -> int:
            pass

        def inter_area(self, box) -> float:
            pass

        def iou(self, box) -> float:
            pass

        def crop(self, image) -> np.ndarray:
            pass

        def draw(self, image, bgr_color=(235, 206, 135)) -> None:
            pass

    class Box:
        @staticmethod
        def create_by_tlhw(t, l, h, w) -> Box_:
            pass

        @staticmethod
        def create_by_ltwh(l, t, w, h) -> Box_:
            pass

        @staticmethod
        def create_by_tlbr(t, l, b, r) -> Box_:
            pass

        @staticmethod
        def create_by_ltrb(l, t, r, b) -> Box_:
            pass


    # direction
    class Direction:
        @staticmethod
        def unit_vector(x, y) -> tuple:
            pass

        def __init__(self, start_x, start_y, end_x, end_y):
            pass

        def angle(self, x, y) -> float:
            pass

        def horizontal_projection_len(self, x, y) -> float:
            pass

        def vertical_projection_len(self, x, y) -> float:
            pass

        def draw(self, image, bgr_color=(0,255,255)):
            pass

    # image
    def b64_to_arr(b64) -> np.ndarray:
        pass

    def arr_to_b64(arr, format='jpeg') -> str:
        pass

    def draw_box_text(img, top, left, height, width, text=None, bgr_color=(235,206,135), thickness=None) -> None:
        pass

    def draw_polygonal(img, xy_list, bgr_color=(0,255,0), thickness=None) -> None:
        pass

    def draw_line(img, x1, y1, x2, y2, bgr_color=(0, 97, 255), thickness=None) -> None:
        pass

    def draw_point(img, x, y, bgr_color=(0,0,255), thickness=None) -> None:
        pass

    def normalize_image(img) -> np.ndarray:
        pass

    def resize_image_scale(image, shape, interpolation=cv2.INTER_LINEAR) -> tuple:# image, scale
        pass

    def letterbox_image(image, shape, interpolation=cv2.INTER_LINEAR) -> np.ndarray:
        pass


    # region_polygonal
    class RegionPolygonal:

        def __init__(self, width, height, xy_list, margin=0.05, min_w=None, max_w=None, min_h=None, max_h=None):
            self.width = 0
            self.height= 0
            self.xy_list = list()
            self.min_w = 0
            self.max_w = 0
            self.min_h = 0
            self.max_h = 0

        def crop_has(self, x, y) -> bool:
            pass

        def has(self, x, y) -> bool:
            pass

        def crop(self, image) -> np.ndarray:
            pass

        def crop_and_fill(self, image) -> np.ndarray:
            pass

        def crop_real_xy(self, x, y) -> tuple:
            pass

        def draw(self, image, bgr_color_polygonal=(0,255,0), draw_box=False, bgr_color_box=(200,255,200)) -> None:
            pass


    def merge_region(region_list):
        pass

    # straight_line
    class StraightLine:
        def __init__(self, x1, y1, x2, y2):
            pass

        @property
        def len(self) -> float:
            pass

        def horizontal_position(self, x, y) -> int:
            pass

        def vertical_position(self, x, y) -> int:
            pass

        def hor_or_ver_position(self, x, y)-> int:
            pass

        def angle(self, x, y) -> float:
            pass

        def horizontal_projection_len(self, x, y) -> float:
            pass

        def vertical_projection_len(self, x, y) -> float:
            pass

        def has(self, x, y) -> bool:
            pass

        def distance(self, x, y) -> float:
            pass

        def get_projection(self, x, y) -> np.ndarray:
            pass

        def draw(self, image, bgr_color=(0,97,255)) -> None:
            pass

    # video_capture
    class FrameMap:
        @staticmethod
        def map(frame, frame_num):
            return frame

        @staticmethod
        def width_map(width, height):
            return width

        @staticmethod
        def height_map(width, height):
            return height


    class VideoCapture:
        def __init__(self, endpoint):
            pass

        @property
        def endpoint(self) -> str:
            pass

        @property
        def device_name(self) -> str:
            pass

        @property
        def cur_frame_num(self) -> int:
            pass

        @property
        def height(self) -> int:
            pass

        @property
        def map_height(self) -> int:
            pass

        @property
        def width(self) -> int:
            pass

        @property
        def map_width(self) -> int:
            pass

        @property
        def frame_map(self) -> FrameMap:
            pass

        @property
        def retrieve_step(self) -> int:
            pass

        @property
        def history_size(self) -> int:
            pass

        @property
        def fps(self) -> int:
            pass

        @property
        def cap_lock(self) -> threading.Lock :
            pass

        @property
        def catch(self) -> dict:
            pass

        def get_frame(self, frame_num) -> np.ndarray:
            pass

        def get_map_frame(self, frame_num) -> np.ndarray:
            pass

        def read(self, is_return_num=False, timeout=8, is_copy=True) -> typing.Any:
            pass

        def read_map(self, is_return_num=False, timeout=8, is_copy=True) -> typing.Any:
            pass

        def read_non_blocking(self, is_return_num=False, is_copy=True) -> typing.Any:
            pass

        def read_map_non_blocking(self, is_return_num=False, is_copy=True) -> typing.Any:
            pass

    def create_cap(endpoint,
               device_name,
               cap_cls=None,
               out_width=None,
               out_height=None,
               args=(),
               frame_map=None,
               reconnect_time=0,
               retrieve_step=1,
               history_size=0,
               map_history_size=0) -> VideoCapture:
        pass


    def read_timeout_callback(endpoint):
        pass


from .box import *
from .image import *
from .direction import *
from .region_polygonal import *
from .straight_line import *
from .video_capture import *
