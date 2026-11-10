import socket

server = socket.socket(
    socket.AF_UNIX,
    socket.SOCK_STREAM
)

socket_path = "/tmp/dozeguard-test.sock"

server.bind(socket_path)
server.listen()

print("Server waiting for connection...")

connection, address = server.accept()

data = connection.recv(1024)

print("Received:", data.decode())

connection.sendall(b"Hello from DozeGuard daemon!")

connection.close()
server.close()