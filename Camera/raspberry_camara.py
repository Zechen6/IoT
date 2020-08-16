import os
import socket
import server
import sys
import time
import json

# server_address = "192.168.0."


def get():  # 获取图片，这里是jpg格式的图片
    import requests
    try:
        img = requests.get('http://192.168.0.111:8080/?action=snapshot&n=1', timeout=1).content
        print(img)
        send_data = img[0:1024]
        print('Get local img success')
        return img
    except:
        print('get snapshot fail')


def send_to_sever(img, sensor, sock, t):


    data = []
    t = bytes(t)
    interval = b'0000000'
    data = bytes(img) + interval + bytes(sensor) + interval + t + interval
    while True:
        # 发送前确认发送次数
        length = len(data)
        # s.connect(server_address)
        sock.sendall("start".encode(encoding="UTF-8"))
        # start = time.time()
        recieve = sock.recv(1024)
        if recieve == b'OK':  # 发送前确认服务器OK
            sock.sendall(str(length).encode(encoding="UTF-8"))
            recieve = sock.recv(1024)
        if recieve == b'YES':  # 发送前确认服务器收到长度信息
            already = 0
            while (length - already) > 0:  # 开始传送
                send_data = data[already:already+1024]
                sock.sendall(send_data)
                already += 1024


def get_sensor_value(client_socket):  # 获取传感器数据

    client_socket.sendall("start".encode(encoding="UTF-8"))
    recv_data = client_socket.recv(1024)
    if recv_data == b'hello from ESP8266\r\n':
        recv_data = client_socket.recv(1024)
    if recv_data == b'A':
        recv_data = client_socket.recv(1024)
    if len(recv_data) < 0:
        recv_data = client_socket.recv(1024)
    return recv_data


def open_camera():  # 打开摄像头
    os.system('sh startup.sh')


if __name__ == '__main__':
    isStop = True
    # 连接设备端——相对于设备端，这是服务器
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("192.168.0.109", 8082))
    serverSocket.listen(5)
    print("等待连接")
    client_socket, client_info = serverSocket.accept()
    # 连接服务器——相对于云端，这是客户端
    server_address = ('127.0.0.1', 8081)  # 服务器地址
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化socket
    s.connect(server_address)  # 建立连接
    # 发送数据
    i = 0
    while isStop:
        i += 1
        send_to_sever(get(), get_sensor_value(client_socket), s, i)
        if i == 65535:  # 对齐数据，防止网络传输过程中顺序错乱
            i = 0
