from threading import Thread, Lock, RLock
from logger_tt import setup_logging
from logging import getLogger


__author__ = "Duc Tin"
setup_logging()
logger = getLogger(__name__)


class MyObject:
    def __repr__(self):
        with RLock():
            return 'my object_locking'


def my_func():
    a = MyObject()
    return a / 3


if __name__ == '__main__':
    my_func()
