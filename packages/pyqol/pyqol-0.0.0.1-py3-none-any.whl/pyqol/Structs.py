
from fastcore.all import store_attr
import functools

#? Dict, but cool
class Struct(object):
    def __init__(self, *args, **kwargs): store_attr()

class Registry():
    """Creates a registry of functions"""
    def __init__(self,):
        self.registry = dict()
    def register(self, f):
        self.registry[f.__name__] = f
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            f(*args, **kwargs)
        return wrapper
    def __getitem__(self, name):
        return self.registry[name]