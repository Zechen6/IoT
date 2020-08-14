import socket
import math


def server():
    server_address = ("127.0.0.1", 8081)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    clientSocket, clientInfo = server_socket.accept()
    recieve_data = b''
    recv_data = clientSocket.recv(1024)
    if recv_data == b'start':
        clientSocket.sendall("OK".encode(encoding="UTF-8"))
        recv_data = clientSocket.recv(1024)
    if len(recv_data) > 0:
        clientSocket.sendall("YES".encode(encoding="UTF-8"))
        round_times = math.ceil(int(recv_data)/1024)
        for i in range(round_times):
            recv_data = clientSocket.recv(1024)
            recieve_data = recieve_data + bytes(recv_data)
        print(recieve_data)


if __name__ == "__main__":
    server()
