
import socket

SOCKET_PATH = "/tmp/dozeguard.sock"

command = input("Enter DozeGuard command: ")

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    client.connect(SOCKET_PATH)
    client.sendall(command.encode())

    response = client.recv(1024)
    print("Daemon:", response.decode())

finally:
    client.close()


