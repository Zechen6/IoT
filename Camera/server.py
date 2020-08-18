import socket
import math
import time
import queue
import threading

# 存储接收到的传感器数据
sensorDataQueue = queue.Queue()
handleDataQueue = queue.Queue()


def recvDataServer():
    # 准备socket
    serverAddress = ("127.0.0.1", 8081)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(serverAddress)

    # 等待客户端连接
    serverSocket.listen(5)

    while True:
        try:
            print("recvDataServer等待连接...")
            tcpSocket, clientInfo = serverSocket.accept()
            print('连接成功')

            # 目前只考虑一个客户端，所以此处不使用多线程
            while True:
                recvData = b''
                # 接收命令
                while True:
                    data = tcpSocket.recv(1024)
                    recvData += data
                    if recvData.endswith(b'\n'):
                        break
                tcpSocket.sendall(b'OK\n')
                if recvData == b'Hello\n':
                    print('client:Hello')
                    continue
                else:
                    length = int(recvData[0:len(recvData) - 1])
                    # print('要传入的数据大小为：' + str(length))

                recvData = b''
                # 接收数据
                while length > 0:
                    data = tcpSocket.recv(1024)
                    length -= len(data)
                    recvData += data
                tcpSocket.sendall(b'OK\n')
                # print("传入的数据" + str(recvData))

                # TODO 处理数据
                sensorDataQueue.put(recvData)
        except ConnectionResetError:
            print("连接断开")


def sendDataServer():
    # 准备socket
    serverAddress = ("127.0.0.1", 8082)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(serverAddress)

    # 等待客户端连接
    print("sendDataServer等待连接...")
    serverSocket.listen(5)

    while True:
        try:
            tcpSocket, clientInfo = serverSocket.accept()
            print('连接成功')

            tcpSocket.sendall(b'Hello\n')
            recvData = b''
            while True:
                data = tcpSocket.recv(1024)
                recvData += data
                if recvData.endswith(b'\n'):
                    break

            while True:
                sendData = handleDataQueue.get()
                # print(sendData)
                length = len(sendData)

                # 发送数据长度
                tcpSocket.sendall(str(length).encode("UTF-8") + b"\n")
                recvData = b''
                while True:
                    data = tcpSocket.recv(1024)
                    recvData += data
                    if recvData.endswith(b'\n'):
                        break

                # 发送所有数据
                tcpSocket.sendall(sendData)
                recvData = b''
                while True:
                    data = tcpSocket.recv(1024)
                    recvData += data
                    if recvData.endswith(b'\n'):
                        break

                time.sleep(1)
        except ConnectionResetError:
            print("断开连接")


def handleDataProc():
    while True:
        # TODO 处理数据
        rawData = sensorDataQueue.get()
        handleData = (str(rawData, encoding="UTF-8") + str(time.time())).encode("UTF-8")
        handleDataQueue.put(handleData)


def main():
    sendDataThread = threading.Thread(target=sendDataServer)
    sendDataThread.start()
    recvDataThread = threading.Thread(target=recvDataServer)
    recvDataThread.start()
    handleDataThread = threading.Thread(target=handleDataProc)
    handleDataThread.start()


if __name__ == "__main__":
    recvDataThread = threading.Thread(target=recvDataServer)
    recvDataThread.start()











