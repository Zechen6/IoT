import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket
import re
import ui
import threading
import raspberry_camara


class MainWidget(QWidget):

    ANGLE = 1
    MUSCLE_STRENGTH = 2
    PHYSIOLOGICAL_FUNCTION = 3
    NUMBER = 4
    HINT = 5

    def __init__(self, parent=None):
        super().__init__()

        # 初始化
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("resource/back.jpg")))
        self.setPalette(palette)

        # 开始界面
        self.start_widget = ui.Start()
        self.start_widget.ui.pushButton.clicked.connect(self.enter_select)

        # 锻炼选择界面
        self.select_widget = ui.Select()
        self.select_widget.ui.listWidget.itemClicked.connect(self.enter_exercise)
        self.select_widget.ui.pushButton.clicked.connect(self.enter_start)

        # 锻炼界面
        self.exercise_widget = ui.Exercise()
        self.exercise_widget.ui.pushButton.clicked.connect(self.enter_start)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.start_widget)
        self.stack.addWidget(self.select_widget)
        self.stack.addWidget(self.exercise_widget)
        self.setLayout(self.stack)
        self.resize(500, 800)

        # 建立与服务器之间的链接
        thread1 = threading.Thread(target=raspberry_camara.sendDataClient)
        thread1.start()
        thread2 = threading.Thread(target=raspberry_camara.recvDataClient)
        thread2.start()

        # 开启摄像头
        # raspberry_camara.openCamera()

        self.listenEvent()

    def enter_select(self):
        print("进入动作选择界面")
        self.stack.setCurrentIndex(1)

    def enter_exercise(self, item):
        print("进入锻炼界面")
        self.exercise_widget.ui.movementName.setText(item.text())
        self.stack.setCurrentIndex(2)
        # TODO 在锻炼界面需要与服务器交互

    def enter_start(self):
        print("进入开始界面")
        self.stack.setCurrentIndex(0)

    # 使用该方法设置锻炼界面中的一些数值和提示信息
    def updateDataOnExercise(self, i, text):
        self.exercise_widget.ui.changeData(i, str(text))

    def listenEvent(self):
        self.thread = Runthread()
        self.thread.signal.connect(self.eventChoose)
        self.thread.start()

    def eventChoose(self, msg):
        # TODO 根据msg更新界面上的信息
        print(msg)
        self.enter_exercise(self.select_widget.ui.listWidget.item(0))


'''
    def listenEvent(self):
        self.thread = Runthread()
        self.thread._signal.connect(self.eventChoose)
        self.thread.start()


    def eventChoose(self, msg):
        if re.search("InfoControll", str(msg)) != None:
            m = str(msg)
            self.updateDataOnExercise(int(m.split('_')[1]), m)
        elif re.search("A",str(msg)) != None:
            self.enter_select()
        elif re.search("B", str(msg)) != None:
            self.enter_start()
        elif re.search("C1", str(msg)) != None:
            self.enter_exercise(self.select_widget.ui.listWidget.item(0))
        elif re.search("C2", str(msg)) != None:
            self.enter_exercise(self.select_widget.ui.listWidget.item(2))
        elif re.search("C3", str(msg)) != None:
            self.enter_exercise(self.select_widget.ui.listWidget.item(3))


class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
        #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("192.168.0.103", 8082))
        except:
            print("连接超时")
        while(1):
            info = client.recv(1024)
            self._signal.emit(str(info))  # 信号发送
            info = ''
'''


class Runthread(QtCore.QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            # TODO 此处还需要添加防止误判的功能
            message = raspberry_camara.getMessages().get()
            # TODO 处理message数据（此处可以调用评分系统来处理）
            self.signal.emit(str(message, encoding="UTF-8"))  # 信号发送


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    sys.exit(app.exec())





