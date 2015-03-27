import logging
from importlib import import_module


def debug(func):
    # @debug is handy when debugging distutils requests
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.exception("@debug")
    return _wrapped


def import_item(name):
    path, item_name = name.rsplit('.', 1)
    mod = import_module(path)
    return getattr(mod, item_name)
