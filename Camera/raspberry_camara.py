import os
import socket
import threading
import time

# server_address = "192.168.0."


# 打开摄像头
def open_camera():
    os.system('sh startup.sh')


# 获取图片，这里是jpg格式的图片
def get():
    import requests
    try:
        img = requests.get('http://192.168.0.111:8080/?action=snapshot&n=1', timeout=1).content
        print(img)
        send_data = img[0:1024]
        print('Get local img success')
        return img
    except:
        print('get snapshot fail')


# 获取传感器数据
def get_sensor_value(client_socket):

    client_socket.sendall("start".encode(encoding="UTF-8"))
    recv_data = client_socket.recv(1024)
    if recv_data == b'hello from ESP8266\r\n':
        recv_data = client_socket.recv(1024)
    if recv_data == b'A':
        recv_data = client_socket.recv(1024)
    if len(recv_data) < 0:
        recv_data = client_socket.recv(1024)
    return recv_data

# t = bytes(t)
# interval = b'0000000'
# data = bytes(img) + interval + bytes(sensor) + interval + t + interval


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
        # TODO 获取数据
        sendData = b'datadatadatadatadatadatadatadatadata'
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
            print('要传入的数据大小为：' + str(length))

        # 接收数据
        recvData = b''
        while length > 0:
            data = clientSocket.recv(1024)
            length -= len(data)
            recvData += data
        clientSocket.sendall(b'OK\n')
        print("传入的数据" + str(recvData))

        # TODO 处理数据


if __name__ == '__main__':
    recvDataThread = threading.Thread(target=recvDataClient)
    recvDataThread.start()
    sendDataThread = threading.Thread(target=sendDataClient)
    sendDataThread.start()
    # isStop = True
    # # 连接设备端——相对于设备端，这是服务器
    # serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # serverSocket.bind(("127.0.0.1", 8082))
    # serverSocket.listen(5)
    # print("等待连接")
    # client_socket, client_info = serverSocket.accept()
    # # 连接服务器——相对于云端，这是客户端
    # server_address = ('127.0.0.1', 8081)  # 服务器地址
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化socket
    # s.connect(server_address)  # 建立连接
    # # 发送数据
    # i = 0
    # while isStop:
    #     i += 1
    #     sendDataToSever(get(), get_sensor_value(client_socket), s, i)
    #     if i == 65535:  # 对齐数据，防止网络传输过程中顺序错乱
    #         i = 0



