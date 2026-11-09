import subprocess

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
                "--why=Active keep-awake session",
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
            