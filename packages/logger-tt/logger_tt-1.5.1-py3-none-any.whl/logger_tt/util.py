import time
import threading
import _thread
from contextlib import contextmanager

__author__ = "Duc Tin"


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException(f'Action took longer than {seconds} seconds!')
    finally:
        timer.cancel()


if __name__ == '__main__':
    try:
        with time_limit(3):
            time.sleep(5)
    except TimeoutException as e:
        print(e)