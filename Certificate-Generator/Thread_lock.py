import threading


class Locker:
    def __init__(self):
        self.lock = threading.Lock()
        self.lock.acquire()
    def __enter__(self):
        return self.lock
    def __exit__(self, type, value, traceback):
        self.lock.release()
        return False