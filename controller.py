from core.session import Session
from backends.linux import LinuxInhibitor


class Controller:
    def __init__(self):
        self.session = Session()
        self.inhibitor = LinuxInhibitor()

    def start(self,minutes=None):
        if self.session.is_active():
            return False
        self.session.start(minutes)

        try:
            self.inhibitor.start()
        except Exception:
            self.session.stop()
            raise

        return True


    def stop(self):
        self.inhibitor.stop()
        self.session.stop()


    def is_active(self):
        active = self.session.is_active()
        if not active:
            self.inhibitor.stop()

        return active


    