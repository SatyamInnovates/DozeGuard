import logging
import time
from core.session import Session
from core.battery_rule import should_stop
from backends.linux import LinuxInhibitor, read_battery

logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, battery_floor=30):

        if not isinstance(battery_floor, int) or not 0 <= battery_floor <= 100:
            raise ValueError(
                "battery_floor must be an integer between 0 and 100"
            )
        self.battery_floor = battery_floor
        self.session = Session()
        self.inhibitor = LinuxInhibitor()
        self.last_battery_check = 0
        self.battery_interval = 20    

# checing

    def start(self, minutes=None):
        if self.session.is_active():
            return False,"A session is already active."
        percent,plugged = read_battery()
        if should_stop(percent,plugged,self.battery_floor):
            logger.warning(
                "session start blocked, reason=battery floor,"
                "percent=%s,plugged=%s",
                percent,
                plugged
            )
            return False,(f"Battery too low {percent:.0f}%"
                          "Connect your charger to start DozeGuard.")
        self.last_battery_check = time.monotonic()
        self.session.start(minutes)

        try:
            self.inhibitor.start()
        except Exception:
            self.session.stop()
            logger.exception("inhibitor failed to start")
            raise

        logger.info("session started, minutes=%s", minutes)
        return True, None

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

    def status(self):
        percent, plugged = read_battery()

        if self.is_active():
            remaining = self.session.remaining_time()

            return (
                "Status: Active\n"
                f"Remaining: {remaining}\n"
                f"Battery: {percent:.0f}%\n"
            )

        return (
        "Status: Idle\n"
        f"Battery: {percent:.0f}%\n"
        )
    def tick(self):
        if not self.is_active():
            return

        now = time.monotonic()
        if now - self.last_battery_check < self.battery_interval:
            return
        self.last_battery_check = now

        percent, plugged = read_battery()
        if should_stop(percent, plugged,self.battery_floor):
            self.stop(f"battery floor, percent={percent}, plugged={plugged}")


    def status(self):
        active = self.is_active()
        percent, plugged = read_battery()

        if active:
            remaining = self.session.remaining()

            if remaining is None:
                remaining_text = "Unlimited"
            else:
                minutes = int(remaining) // 60
                seconds = int(remaining) % 60
                remaining_text = f"{minutes:02d}:{seconds:02d}"

            status_text = "Status: Active"
        else:
            remaining_text = "None"
            status_text = "Status: Idle"

        battery_text = (
            f"{percent:.0f}%" if percent is not None else "Unavailable"
        )

        charging_text = "Charging" if plugged else "Not charging"

        return (
            f"{status_text}\n"
            f"Remaining: {remaining_text}\n"
            f"Battery: {battery_text} ({charging_text})"
        )