# @Time   : 2019-01-29
# @Author : zhangxinhao
if False:
    from typing import Any
    import numpy as np
    import redis


    # local_redis
    def redis_conn(index=None) -> redis.Redis:
        pass

    def get_redis_socket_timeout() -> int:
        pass

    def set_redis_socket_timeout(socket_timeout) -> None:
        pass

    # client
    class Response:
        mq_id = None  # type: str
        data = None  # type: str
        conn_index = None # type: int
        result_protocol = None  # type: str

        def get(self) -> Any:
            pass

    def invoke(url, request, index=None) -> Response:
        pass

    def invoke_cpp(url, request, index=None) -> Response:
        pass

    class Request:
        data = None # type: Any
        mq_id = None # type: str

    # server
    class Request:
        url = None  # type: str
        mq_id = None  # type: str
        data = None  # type: str
        conn_index = None  # type: int
        result_protocol = None  # type: str


    def initialize(*args, **kwargs) -> Any:
        pass


    def start_simple_server(thread_num=1) -> None:
        pass


    def start_distributed_server(thread_num=1) -> None:
        pass


    # context
    request = None # type: Request
    response = None # type: Response
    catch = None # type: dict

    # route
    PHASE_BEFORE = "BEFORE"
    PHASE_DURING = "DURING"
    PHASE_AFTER = "AFTER"

    def response_route(url, phase=PHASE_DURING) -> Any:
        pass


    def add_response_route(url, func, phase=PHASE_DURING) -> None:
        pass


from .local_redis import *
from .client import *
from .context import *
from .route import *
from .server import *
