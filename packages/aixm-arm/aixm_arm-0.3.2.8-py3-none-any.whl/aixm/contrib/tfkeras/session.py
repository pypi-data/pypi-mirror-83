# @Time   : 2018-9-10
# @Author : zhangxinhao
import os
import tensorflow as tf

try:
    tf.ConfigProto
    def create_sess(cuda='0', gpu_mem=0.2, allow_growth=False, is_interactive_session=True):
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda
        if allow_growth:
            tf_config = tf.ConfigProto(log_device_placement=False,
                                       allow_soft_placement=True,
                                       gpu_options=tf.GPUOptions(allow_growth=True))
        else:
            tf_config = tf.ConfigProto(log_device_placement=False,
                                       allow_soft_placement=True,
                                       gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=gpu_mem))
        if is_interactive_session:
            return tf.InteractiveSession(config=tf_config)
        return tf.Session(config=tf_config)

except:
    def create_sess(cuda='0', gpu_mem=0.2, allow_growth=False, is_interactive_session=True):
        os.environ["CUDA_VISIBLE_DEVICES"] = cuda
        if allow_growth:
            tf_config = tf.compat.v1.ConfigProto(log_device_placement=False,
                                       allow_soft_placement=True,
                                       gpu_options=tf.compat.v1.GPUOptions(allow_growth=True))
        else:
            tf_config = tf.compat.v1.ConfigProto(log_device_placement=False,
                                       allow_soft_placement=True,
                                       gpu_options=tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=gpu_mem))
        if is_interactive_session:
            return tf.compat.v1.InteractiveSession(config=tf_config)
        return tf.compat.v1.Session(config=tf_config)

__all__ = ['create_sess']
