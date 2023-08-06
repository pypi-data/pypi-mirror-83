import time


class CoStrOb:
    def __init__(self, delay: [float, int] = 0.0, true_on_init: bool = True):
        self.delay = delay
        self.last = None if true_on_init else time.time()

    def __bool__(self):
        if self.last is None or time.time() - self.last > self.delay:
            self.last = time.time()
            return True
        else:
            return False
