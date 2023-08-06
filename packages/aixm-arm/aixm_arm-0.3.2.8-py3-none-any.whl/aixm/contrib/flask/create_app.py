# @Time   : 2019-01-11
# @Author : zhangxinhao
from flask import Flask
from aixm.utils import get_class_or_func


def create_app(setting_module, register_func, init_func=None):
    app = Flask(__name__)
    app.config.from_object(setting_module)
    if init_func is not None:
        get_class_or_func(init_func)()

    register = get_class_or_func(register_func)
    register(app)

    if app.config.get('JOBS') is not None:
        from flask_apscheduler import APScheduler
        apscheduler = APScheduler()
        apscheduler.init_app(app)
        apscheduler.start()
    return app


__all__ = ['create_app']