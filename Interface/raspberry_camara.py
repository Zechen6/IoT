import os
import socket
import threading
import time
import queue

sensorData = None
messages = queue.Queue()


# 打开摄像头
def openCamera():
    os.system('sh startup.sh')


# 获取图片，这里是jpg格式的图片
def getImg():
    import requests
    try:
        img = requests.get('http://192.168.0.111:8080/?action=snapshot&n=1', timeout=1).content
        print(img)
        print('Get local img success')
        return img
    except:
        print('get snapshot fail')


# 获取传感器数据
def recvSensorData():
    # TODO 与传感器连接
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("127.0.0.1", 8082))
    serverSocket.listen(5)
    print("等待连接")
    client_socket, client_info = serverSocket.accept()
    client_socket.sendall("start".encode(encoding="UTF-8"))
    recv_data = client_socket.recv(1024)
    if recv_data == b'hello from ESP8266\r\n':
        recv_data = client_socket.recv(1024)
    if recv_data == b'A':
        recv_data = client_socket.recv(1024)
    if len(recv_data) < 0:
        recv_data = client_socket.recv(1024)
    return recv_data


# 获取数据
def getData():
    # TODO 刘泽晨
    return b'datatata'


def sendDataClient():
    # 准备socket
    serverAddress = ('127.0.0.1', 8081)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("等待连接....")
    clientSocket.connect(serverAddress)  # 建立连接

    # 互相发送Hello消息
    clientSocket.sendall(b'Hello\n')
    data = b''
    while True:
        recvData = clientSocket.recv(1024)
        data += recvData
        if data.endswith(b'\n'):
            break

    while True:
        sendData = getData()
        length = len(sendData)

        # 发送数据长度
        clientSocket.sendall(str(length).encode(encoding="UTF-8") + b'\n')
        data = b''
        while True:
            recvData = clientSocket.recv(1024)
            data += recvData
            if data.endswith(b'\n'):
                break

        # 发送数据
        clientSocket.sendall(sendData)
        data = b''
        while True:
            recvData = clientSocket.recv(1024)
            data += recvData
            if data.endswith(b'\n'):
                break

        # 暂停
        time.sleep(1)


def recvDataClient():
    # 准备socket
    serverAddress = ('127.0.0.1', 8082)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("等待连接....")
    clientSocket.connect(serverAddress)  # 建立连接

    while True:
        # 接收命令
        recvData = b''
        while True:
            data = clientSocket.recv(1024)
            recvData += data
            if recvData.endswith(b'\n'):
                break
        clientSocket.sendall(b'OK\n')
        if recvData == b'Hello\n':
            print('server:Hello')
            continue
        else:
            length = int(recvData[0:len(recvData) - 1])
            # print('要传入的数据大小为：' + str(length))

        # 接收数据
        recvData = b''
        while length > 0:
            data = clientSocket.recv(1024)
            length -= len(data)
            recvData += data
        clientSocket.sendall(b'OK\n')
        # print("传入的数据" + str(recvData))

        # 处理数据
        messages.put(recvData)


def getMessages():
    return messages


if __name__ == '__main__':
    # recvDataThread = threading.Thread(target=recvDataClient)
    # recvDataThread.start()
    sendDataThread = threading.Thread(target=sendDataClient)
    sendDataThread.start()



