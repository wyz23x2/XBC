import ifix
from main import *
from utils import *
import sys
try:
    import threading
except Exception:
    threading = None
# XXX threading is restricted by the GIL of Python, hence suboptimal
class ThreadNotEnded(Exception):
    pass
class Thread:
    def __init__(self, func, args=(), kwargs=None, name=None):
        kwargs = kwargs or {}
        self.a, self.f, self.k = args, func, kwargs
        def f(s, fn, a, k):
            s.r = fn(*a, **k)
        if threading:
            self.t = threading.Thread(target=f, args=(self, func, args, kwargs), name=name, daemon=True)
        else:
            self.t = f
        self.r = ThreadNotEnded()
    def start(self):
        if threading:
            self.t.start()
        elif isinstance(self.r, ThreadNotEnded):
            self.run()
        else:
            raise RuntimeError('threads can only be started once')
    def run(self):
        if threading:
            self.t.run()
        else:
            self.t(self, self.f, self.a, self.k)
    def returned(self):
        if isinstance(self.r, ThreadNotEnded):
            raise self.r
        return self.r
def setswitchinterval(interval):
    sys.setswitchinterval(interval)

if __name__ == '__main__':
    def test():
        for _ in range(9000000): pass
        print('5')
        return 5
    t = Thread(test)
    t.start()
    print('3')
    while True:
        try:
            print(t.returned())
        except Exception:
            continue
        else:
            break
