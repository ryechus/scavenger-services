import functools

from image_service.core.logging import logger


def silent_connection(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            logger.warning("Can't connect to redis")

    return wrapper
