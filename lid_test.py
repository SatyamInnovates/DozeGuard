
import time
from datetime import datetime

print("Lid test started. Press Ctrl+C to stop.")

try:
    while True:
        timestamp = datetime.now().astimezone()
        with open("lid_test.log", "a") as file:
            file.write(timestamp.strftime("%A %d %B %Y %I:%M:%S %p %Z") + "\n")

        time.sleep(5)

except KeyboardInterrupt:
    print("Lid test stopped.")

