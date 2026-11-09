import subprocess

class LinuxInhibitor:
    def __init__(self):
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen([
            "systemd-inhibit", "--what=sleep", "--who=DozeGuard",
            "--why=session", "sleep", "infinity"
        ])

    def stop(self):
        if self.proc is not None:
            self.proc.terminate()
            self.proc = None