# -*- coding:utf-8 -*-


# @version: 1.0
# @author: luojie
# @date: '14-9-5'


class Reflector(object):
    def __init__(self):
        pass

    @staticmethod
    def get_instance(class_path, class_name="", *args):
        if class_name:
            module = __import__(class_path, fromlist=['any_str'])
        else:
            parts = class_path.split(".")
            class_path = ".".join(parts[:-1])
            class_name = parts[-1]
            module = __import__(class_path, fromlist=['any_str'])
        return getattr(module, class_name)(*args)

    @staticmethod
    def get_method(instance, method_name):
        return getattr(instance, method_name)

    @staticmethod
    def get_static_method(module_path, method_name):
        module = __import__(module_path, fromlist=['any_str'])
        return getattr(module, method_name)

    @staticmethod
    def get_class(class_path, class_name=""):
        if class_name:
            module = __import__(class_path, fromlist=['any_str'])
        else:
            parts = class_path.split(".")
            class_path = ".".join(parts[:-1])
            class_name = parts[-1]
            module = __import__(class_path, fromlist=['any_str'])
        return getattr(module, class_name)


if __name__ == "__main__":
    pass
