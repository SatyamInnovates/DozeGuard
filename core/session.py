import time


class Session:

    def __init__(self):
        self.active = False
        self.deadline = None

    def start(self,minutes=None): 
        self.active = True
        if minutes is None:
            self.deadline = None
        else:
            self.deadline = time.monotonic() + minutes*60


    def stop(self):
        self.active = False
        self.deadline = None

    def is_active(self):
        if self.active and self.deadline is not None:
            if time.monotonic() >= self.deadline:
                self.stop()
        return self.active

    
    def remaining(self):
        if not self.is_active() or self.deadline is None:
            return None
        return self.deadline - time.monotonic()



