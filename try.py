from controller import Controller

c = Controller()

c.start(minutes=1)

print("DozeGuard is active!")

try:
    input("Press Enter to stop DozeGuard...")
finally:
    c.stop()
    print("DozeGuard stopped!")


