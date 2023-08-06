# @Time   : 2019-05-21
# @Author : zhangxinhao
from .session import *
from .dataset import *
if False:
    def read_images(image_path_list,
                    label_list,
                    batch_size,
                    out_shape,
                    image_channels=3,
                    init_shape=None,
                    is_random_rotate=False,
                    is_random_crop=False,
                    is_random_flip=False,
                    is_standardization=False,
                    other_tf_operations=None,
                    test_ratio=0.1,
                    max_test_num=1500,
                    num_threads=4) -> tuple:
        # train_batch(tuple), test_batch(tuple)
        pass


    def get_image_path_and_label(root_dir, formats=('jpg', 'jpeg')) -> tuple:
        # image_paths, labels, label_num_to_label, label_to_label_num
        pass


    def create_sess(cuda='0', gpu_mem=0.2, allow_growth=False, is_interactive_session=True):
        pass


