import inspect
from functools import wraps

def singleton(cls):
    instances = dict()
    @wraps(cls)
    def wrap(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrap

@singleton
class MetaprogrammingExample:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr_name):
        if attr_name.startswith("dynamic_method_"):
            def dynamic_method():
                return f"Dynamic method {attr_name} called"
            return dynamic_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr_name}'")

def main():
    meta = MetaprogrammingExample("example")
    print(meta.name)
    print(meta.dynamic_method_dynamic_method_1())
    try:
        print(meta.non_existent_method())
    except AttributeError as e:
        print(e)

if __name__ == "__main__":
    main()
# NEXUS-ONE CORE MODULE