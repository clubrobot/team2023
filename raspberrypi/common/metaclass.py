#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Singleton(type):
    """
    Singleton Class
    Usage:
        class MyClass(metaclass=Singleton):
            pass
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Final(type):
    """
    Final Class to avoid class inheritance
    Usage:
        class MyClass(metaclass=Final):
            pass
    """
    def __new__(cls, name, bases, classdict):
        for b in bases:
            if isinstance(b, Final):
                raise TypeError("""type '{0}' is not an acceptable base type.
                You can't create a inherited class due to the Final protection.
                Please take a look at the mother's documentation.""".format(b.__name__))
        return type.__new__(cls, name, bases, dict(classdict))
