import subprocess
import psutil
import logging


MARKER = "--why=DozeGuard keep-awake session"

class LinuxInhibitor:
    def __init__(self):
        self.proc = None

    def start(self):
        if self.proc is not None and self.proc.poll() is None:
            return

        
        self.proc = subprocess.Popen(
            [
                "systemd-inhibit",
                "--what=sleep",
                "--who=DozeGuard",
                "--why=DozeGuard keep-awake session",
                "--mode=block",
                "sleep",
                "infinity",
            ]
        )



    def stop(self):
        if self.proc is not None:
            if self.proc.poll() is None:
                self.proc.terminate()

                try:
                    self.proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait()

            self.proc = None

    
                 
def cleanup_orphans():
    ended = 0
    for proc in psutil.process_iter(["cmdline"]):
        cmd = proc.info["cmdline"] or []
        if MARKER in cmd:
            try:
                proc.terminate()
                ended += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    return ended


def read_battery():
    b = psutil.sensors_battery()
    if b is None:
        return None,True
    return b.percent,b.power_plugged
