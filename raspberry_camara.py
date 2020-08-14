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


def send_to_sever(img):
    count = 0
    server_address = ('127.0.0.1', 8081)  # 服务器地址
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 初始化socket
    s.connect(server_address)  # 建立连接
    while True:
        if count == 0:  # 发送前确认发送次数
            length = len(img)
            # s.connect(server_address)
            s.sendall("start".encode(encoding="UTF-8"))
            # start = time.time()
            recieve = s.recv(1024)
            if recieve == b'OK':  # 发送前确认服务器OK
                s.sendall(str(length).encode(encoding="UTF-8"))
                recieve = s.recv(1024)
            if recieve == b'YES':  # 发送前确认服务器收到长度信息
                already = 0
                while (length - already) > 0: # 开始传送
                    send_data = img[already:already+1024]
                    s.sendall(send_data)
                    already += 1024


def open_camera():  # 打开摄像头
    os.system('sh startup.sh')


if __name__ == '__main__':
    isStop = True
    while isStop:
        send_to_sever(get())
