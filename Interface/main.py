import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import time
import ui
import threading
import raspberry_camara

suggestions = [
    [
        "不要在最低点放松手臂,保持发力，加油",
        "保持胳膊肘的稳定，不要跟随哑铃上抬",
        "肘部不要向外延伸，请保持和身体平面垂直"
    ],
    [
        "不要耸肩！！！",
        "请保持两边肩膀高度一致！！！！",
        "重量过大，请立刻停止！！！！！"
    ]
]


class MainWidget(QWidget):

    ANGLE = 1
    MUSCLE_STRENGTH = 2
    PHYSIOLOGICAL_FUNCTION = 3
    NUMBER = 4
    HINT = 5

    NORMAL_BUTTON = "border:none;background-color:transparent"
    FOCUS_BUTTON = NORMAL_BUTTON + ";" + "color:yellow"

    def __init__(self, parent=None):
        super().__init__()

        # 当前所在控件
        self.index = 0

        # 初始化
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("resource/back.jpg")))
        self.setPalette(palette)

        # 开始界面
        self.start_widget = ui.Start()
        self.start_widget.ui.button_exercise.clicked.connect(self.enter_select)

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
        # thread1 = threading.Thread(target=raspberry_camara.sendDataClient)
        # thread1.start()
        # thread2 = threading.Thread(target=raspberry_camara.recvDataClient)
        # thread2.start()
        thread3 = threading.Thread(target=raspberry_camara.recvDataClient2)
        thread3.start()

        # 开启摄像头
        raspberry_camara.openCamera()

        self.listenEvent()

        self.enter_start()

    def enter_start(self):
        print("进入开始界面")
        self.index = 1
        self.stack.setCurrentIndex(0)
        self.start_widget.ui.button_exercise.setStyleSheet(self.FOCUS_BUTTON)

    def enter_select(self):
        print("进入动作选择界面")
        self.index = 1
        self.stack.setCurrentIndex(1)
        self.select_widget.ui.listWidget.item(0).setForeground(QColor(255, 255, 0))

    def enter_exercise(self, item):
        print("进入锻炼界面")
        self.exercise_widget.ui.movementName.setText(item.text())
        self.stack.setCurrentIndex(2)
        # TODO 在锻炼界面需要与服务器交互

    # 使用该方法设置锻炼界面中的一些数值和提示信息
    def updateDataOnExercise(self, i, text):
        # self.exercise_widget.ui.changeData(i, str(text))
        if i == self.HINT:
            self.exercise_widget.ui.hint.setText(text)
        elif i == self.ANGLE:
            self.exercise_widget.ui.angle.setText(text + "/100")
        elif i == self.MUSCLE_STRENGTH:
            self.exercise_widget.ui.muscleStrength.setText(text + "/100")
        elif i == self.PHYSIOLOGICAL_FUNCTION:
            self.exercise_widget.ui.physiologicalFunction.setText(text + "/100")
        elif i == self.NUMBER:
            self.exercise_widget.ui.number.setText(text)

    def listenEvent(self):
        self.thread = Runthread()
        self.thread.signal.connect(self.eventChoose)
        self.thread.start()

    def down(self):
        curIndex = self.stack.currentIndex()
        if curIndex == 0 and self.index != 3:
            self.start_widget.widget[self.index - 1].setStyleSheet(self.NORMAL_BUTTON)
            self.index += 1
            self.start_widget.widget[self.index - 1].setStyleSheet(self.FOCUS_BUTTON)
        elif curIndex == 1 and self.index != self.select_widget.ui.listWidget.count():
            self.select_widget.ui.listWidget.item(self.index - 1).setForeground(QColor(255, 255, 255))
            self.index += 1
            self.select_widget.ui.listWidget.item(self.index - 1).setForeground(QColor(255, 255, 0))
            self.select_widget.ui.listWidget.scrollToItem(self.select_widget.ui.listWidget.item(self.index - 1))

    def up(self):
        curIndex = self.stack.currentIndex()
        if curIndex == 0 and self.index != 1:
            self.start_widget.widget[self.index - 1].setStyleSheet(self.NORMAL_BUTTON)
            self.index -= 1
            self.start_widget.widget[self.index - 1].setStyleSheet(self.FOCUS_BUTTON)
        elif curIndex == 1 and self.index != 1:
            self.select_widget.ui.listWidget.item(self.index - 1).setForeground(QColor(255, 255, 255))
            self.index -= 1
            self.select_widget.ui.listWidget.item(self.index - 1).setForeground(QColor(255, 255, 0))
            self.select_widget.ui.listWidget.scrollToItem(self.select_widget.ui.listWidget.item(self.index - 1))

    def eventChoose(self, msg: str):
        # TODO 根据msg更新界面上的信息
        curIndex = self.stack.currentIndex()
        if msg == "back":
            if curIndex != 0:
                self.stack.setCurrentIndex(curIndex - 1)
            else:
                print("退出")
        elif msg == "enter":
            print("进入")
            if curIndex == 0 and self.index == 1:
                self.enter_select()
            elif curIndex == 1:
                self.enter_exercise(self.select_widget.ui.listWidget.item(self.index))
        elif msg == "up":
            self.up()
        elif msg == "down":
            self.down()
        else:
            if curIndex != 2:
                return
            if msg[0] == ":":
                i = int(msg[1:])
                if i >= len(suggestions[self.index]):
                    return
                self.updateDataOnExercise(i=self.HINT, text=suggestions[self.index][i])
            else:
                l = msg.split(' ')
                for i in range(4):
                    self.updateDataOnExercise(i=i+1, text=l[i])

'''
ANGLE = 1
MUSCLE_STRENGTH = 2
PHYSIOLOGICAL_FUNCTION = 3
NUMBER = 4
'''

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
            # 此处还需要添加防止误判的功能
            message = raspberry_camara.getMessages().get()
            # 处理message数据（此处可以调用评分系统来处理）
            # print("发送消息")
            self.signal.emit(str(message, encoding="UTF-8"))  # 信号发送


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    sys.exit(app.exec())





