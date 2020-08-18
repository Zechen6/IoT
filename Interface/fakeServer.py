import socket
import time
import queue
import threading

handleDataQueue = queue.Queue()

def sendDataServer():
    # 准备socket
    serverAddress = ("127.0.0.1", 8083)
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

if __name__ == '__main__':
    thread = threading.Thread(target=sendDataServer)
    thread.start()
    while True:
        msg = input("输入msg：")
        handleDataQueue.put(msg.encode("UTF-8"))
