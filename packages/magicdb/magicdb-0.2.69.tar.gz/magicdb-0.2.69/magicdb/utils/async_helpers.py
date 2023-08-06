import concurrent.futures

import asyncio
from functools import wraps

_DEFAULT_POOL = concurrent.futures.ThreadPoolExecutor()
_DEFAULT_POOL._max_workers = max(_DEFAULT_POOL._max_workers, 20)


def threadpool_asyncio(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        future = (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
        return asyncio.wrap_future(future)

    return wrap


def threadpool(f, executor=None):
    @wraps(f)
    def wrap(*args, **kwargs):
        future = (executor or _DEFAULT_POOL).submit(f, *args, **kwargs)
        return future

    return wrap
