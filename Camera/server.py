import socket
import math
import time
import queue
import threading

# 存储接收到的传感器数据
sensorDataQueue = queue.Queue()
handleDataQueue = queue.Queue()
address = "192.168.0.109"

def recvDataServer():
    # 准备socket
    serverAddress = ("192.168.0.109", 8081)
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

                sensorDataQueue.put(recvData)
        except ConnectionResetError:
            print("连接断开")


def sendDataServer():
    # 准备socket
    serverAddress = ("192.168.0.109", 8082)
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
        handleData = getImgFromBytes(rawData)
        sensorData = getSensorData(rawData)
        # handleData = (str(rawData, encoding="UTF-8") + str(time.time())).encode("UTF-8")
        handleDataQueue.put(handleData)


def getImgFromBytes(rawData):
    length = len(rawData)
    img = rawData[0:length-1024]
    fileName = "x.jpg"
    with open(fileName, 'wb') as file:
        file.write(img)
        file.close()
    return img


def getSensorData(rawData):
    length = len(rawData)
    sensorData = rawData[length-1024:length - 1]
    sensorData = str(sensorData, "utf-8")
    sensorData = operateSensorData(sensorData)
    # print(sensorData)
    return sensorData


def operateSensorData(sensorData):
    res = []
    ax = 0
    ay = 0
    az = 0
    gx = 0
    gy = 0
    gz = 0
    muscle = 0
    count = 0
    X = sensorData.split('\n')
    for i in X:
        try:
            count += 1
            ax = ax + int(i.split('\t')[1])
            ay = ay + int(i.split('\t')[2])
            az = az + int(i.split('\t')[3])
            gx = gx + int(i.split('\t')[4])
            gy = gy + int(i.split('\t')[5])
            gz = gz + int(i.split('\t')[6])
            muscle = muscle + int(i.split('\t')[7])
            sum_ = [ax, ay, az, gx, gy, gz, muscle]
        except:

            continue
    # print([ax / count, ay / count, az / count, gx / count, gy / count, gz / count, muscle / count])
    return [ax / count, ay / count, az / count, gx / count, gy / count, gz / count, muscle / count]

def main():
    sendDataThread = threading.Thread(target=sendDataServer)
    sendDataThread.start()
    recvDataThread = threading.Thread(target=recvDataServer)
    recvDataThread.start()
    handleDataThread = threading.Thread(target=handleDataProc)
    handleDataThread.start()


if __name__ == "__main__":
    main()











