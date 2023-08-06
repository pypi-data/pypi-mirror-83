# @Time   : 2019-01-09
# @Author : zhangxinhao
from flask import request


class JsonRequest:
    def __init__(self):
        self.request_data = request.get_json()

    def get(self, keys, default=None, allow_empty=False, raise_exption_if_none=True):
        if isinstance(keys, str):
            keys = [keys]
        else:
            keys = list(keys)

        value = None
        for key in keys:
            v = self.request_data.get(key)
            if v is not None:
                value = v
                break

        if value == "" and not (allow_empty):
            value = None

        if value is None:
            if default is not None:
                return default
            else:
                if raise_exption_if_none:
                    raise Exception('key not exist')
        return value


__all__ = ['JsonRequest']
