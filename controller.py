import logging
import time

from core.session import Session
from core.battery_rule import should_stop
from backends.linux import LinuxInhibitor, read_battery

logger = logging.getLogger(__name__)



class Controller:
    def __init__(self):
        self.session = Session()
        self.inhibitor = LinuxInhibitor()
        self.last_battery_check = 0
        self.battery_interval = 20

    def start(self, minutes=None):
        if self.session.is_active():
            return False

        self.last_battery_check = 0          
        self.session.start(minutes)

        try:
            self.inhibitor.start()
        except Exception:
            self.session.stop()
            logger.exception("inhibitor failed to start")
            raise

        logger.info("session started, minutes=%s", minutes)
        return True

    def stop(self, reason="manual"):
        was_active = self.session.active
        self.inhibitor.stop()
        self.session.stop()
        if was_active:                   
            logger.info("session stopped, reason=%s", reason)

    def is_active(self):
        was_active = self.session.active
        active = self.session.is_active()    
        if not active:
            self.inhibitor.stop()
            if was_active:
                logger.info("session stopped, reason=timer expired")
        return active

    def tick(self):
        if not self.is_active():
            return

        now = time.monotonic()
        if now - self.last_battery_check < self.battery_interval:
            return
        self.last_battery_check = now

        percent, plugged = read_battery()
        if should_stop(percent, plugged):
            self.stop(f"battery floor, percent={percent}, plugged={plugged}")