# -*- coding: utf-8 -*-
""" Base module

    Here is the location of the base class for all other classes and some functions.

    Logging and singleton are defined here.

"""


import os

import logging
import collections


logging.basicConfig(level=logging.INFO,
                    format='%(name)-18s \t %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',)


class Base(object):
    """ Base class

    All classes inherit form this class.
    For now each class get a logger.

    """

    def __init__(self, name):
        self.class_name = name
        #self.io = MyLogger(name)

    @property
    def io(self):
        return logging.getLogger(self.class_name)

    def debug(self, msg):
        self.io.debug(msg)

    def info(self, msg):
        self.io.info(self, msg)

    def warn(self, msg):
        self.io.warn(msg)

    def error(self, msg):
        self.io.error(msg)

    def unknown_error(self):
        self.io.error("Unknown Error occured o_O")


class AttrDict(dict):
    """Dictionary which items can also be addressed by attribute lookup in addition to item lookup"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def IsIterable(obj):
    """ Check if an object is iterable. Come on. The name does say it all!

    Parameters
    ----------
    obj

    Returns
    -------

    """
    if isinstance(obj, collections.Iterable):
        return True
    else:
        return False


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)


def absolute_path(file):
    """ Returns the absolute path of a file if not already passed

    Args:
        file: filename (should better exist)

    Returns:
        absolute path to file
    """
    if os.path.isabs(file):
        return file
    else:
        return os.getcwd() + '/' + file
