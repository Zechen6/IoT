import random
import socket
import math
import time
import queue
import threading
import sys

from PIL import Image

sys.path.append('/home/kmx/openpose/build/examples/tutorial_api_python/')
import posestimate

sys.path.append('/home/kmx/realtime_gesture_recog/')
import recog
import cv2
import numpy as np

# 存储接收到的传感器数据
sensorDataQueue = queue.Queue()
handleDataQueue = queue.Queue()
sendCommandQueue = queue.Queue()
address = "192.168.0.231"

rec = recog.recognizer()
# 手势对应指令字典
gesture_dict = {0: "enter", 1: "up", 2: "back", 3: "down", 4: "\n", 5: "\n"}
gesture_send_frequency = 1
gesture_double_check = [-1, -1]  # 两次识别结果相同时才发送指令
idx_double_check = 0
cur_frequency = 0

success_enter = 0  # 等于2时，进入运动界面

# DEBUG
debug_flag = 0


def recvDataServer():
    # 准备socket
    serverAddress = (address, 8081)
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


def sendCommandServer():
    # 准备socket
    serverAddress = (address, 8083)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(serverAddress)

    # 等待客户端连接
    print("sendCommandServer等待连接...")
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
                sendData = sendCommandQueue.get()
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


def sendDataServer():
    # 准备socket
    serverAddress = (address, 8082)
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
    global success_enter
    global rec

    fre = 0
    advice = 0
    while True:
        # TODO 处理数据
        fre += 1
        rawData = sensorDataQueue.get()
        # 图片测试
        # handleData = getImgFromBytes(rawData)
        print("handling data", fre)
        # 得到识别结果
        handleData = getScoreFromImgBytes(rawData, rec)
        if fre >= 5 and success_enter >= 2:
            genRandomScore()
            genAdvice(advice)
            advice += 1
            fre = 0

        # sensorData = getSensorData(rawData)
        # handleData = (str(rawData, encoding="UTF-8") + str(time.time())).encode("UTF-8")
        handleDataQueue.put(handleData)


def genAdvice(state):
    if state == 0:
        sendCommandQueue.put(":4".encode("UTF-8"))
    elif state == 1:
        sendCommandQueue.put(":3".encode("UTF-8"))
    else:
        suggest_no = random.randint(0, 2)
        command = ":" + str(suggest_no)
        sendCommandQueue.put(command.encode("UTF-8"))


def getImgFromBytes(rawData):
    length = len(rawData)
    img = rawData[0:length - 1024]
    fileName = "x.jpg"
    with open(fileName, 'wb') as file:
        file.write(img)
        file.close()
    return img


def genRandomScore(low=75, high=95):
    scores = np.random.randint(low, high, 4)
    command = " ".join(str(num) for num in scores)
    print("scores:", command)
    sendCommandQueue.put(command.encode("UTF-8"))


def getScoreFromImgBytes(rawData, rec):
    global cur_frequency, success_enter, gesture_double_check, idx_double_check

    length = len(rawData)
    img = rawData[0:length - 1024]
    fileName = "x.jpg"
    with open(fileName, 'wb') as file:
        file.write(img)
        file.close()

    # 手势识别
    cur_frequency += 1
    if cur_frequency == gesture_send_frequency and success_enter < 2:
        img = cv2.imread("x.jpg")
        np_img = np.array(img)
        mask_img = rec.get_hand_img(np_img, 0, 0, fix=True)
        result = rec.recognize(mask_img)
        print("gesture result predict:", gesture_dict[result])
        cur_frequency = 0

        gesture_double_check[idx_double_check] = gesture_dict[result]
        idx_double_check = 1 - idx_double_check
        print(gesture_double_check)

        if gesture_dict[result] == 'enter' and gesture_double_check[0] == gesture_double_check[1] :
            success_enter += 1
        elif gesture_dict[result] == 'back' and gesture_double_check[0] == gesture_double_check[1]:
            success_enter -= 1
            success_enter = 0 if success_enter < 0 else success_enter


        # DEBUG
        global debug_flag
        save_img = Image.fromarray(mask_img)
        save_img.save(str(debug_flag) + ".jpg")
        debug_flag += 1
        # end DEBUG

        if gesture_double_check[0] == gesture_double_check[1]:
            print("send command: ",gesture_dict[result])
            sendCommandQueue.put(gesture_dict[result].encode("UTF-8"))

    # point为获取的节点
    # pose = posestimate.posestimate()
    # point = pose.handle_img(fileName)
    #
    # # 对应 4 5 6 节点，右手三个骨架点
    # hand1 = point[0][4]
    # hand2 = point[0][5]
    # hand3 = point[0][6]
    #
    # score1_x = 1 - (abs(hand1[0] - hand2[0]) - 50) / 50
    # score2_x = 1 - (abs(hand2[0] - hand3[0]) - 25) / 25
    # score_x = (score1_x ** 2 + score2_x ** 2) ** 0.5
    #
    # score1_y = 1 - (abs(hand1[1] - hand2[1]) - 60) / 60
    # score2_y = 1 - (abs(hand2[1] - hand3[1]) - 20) / 20
    # score_y = (score1_y ** 2 + score2_y ** 2) ** 0.5
    #
    # score_z = (hand1[2] + hand2[2] + hand3[2]) / 3
    #
    # score = (score_x + score_y + score_z) / 3
    # return [score_x, score_y, score_z, score]

    return [0, 0, 0, 0]


def getSensorData(rawData):
    length = len(rawData)
    sensorData = rawData[length - 1024:length - 1]
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
    sendCommandThread = threading.Thread(target=sendCommandServer)
    sendCommandThread.start()


if __name__ == "__main__":
    main()
