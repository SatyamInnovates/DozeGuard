from backends.linux import LinuxInhibitor
import time
h = LinuxInhibitor()
h.start()
time.sleep(10)     
h.stop()
