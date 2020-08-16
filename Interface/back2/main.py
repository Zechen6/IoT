import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket
import _signal
import _thread
import ui
import re

class MainWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.resize(500,800)
        self.listenEvent()

    def enter_select(self):
        print("进入动作选择界面")
        self.stack.setCurrentIndex(1)

    def enter_exercise(self, item):
        print("进入锻炼界面")
        self.exercise_widget.ui.movementName.setText(item.text())
        self.stack.setCurrentIndex(2)

    def enter_start(self):
        print("进入开始界面")
        self.stack.setCurrentIndex(0)

    def listenEvent(self):
        self.thread = Runthread()
        self.thread._signal.connect(self.eventChoose)
        self.thread.start()

    def eventChoose(self,msg):
        if re.search("InfoControll", str(msg)) != None:
            self.enter_exercise(self.select_widget.ui.listWidget.item(4))
        elif re.search("A",str(msg)) != None:
            self.enter_select()
        elif re.search("B", str(msg)) != None:
            self.enter_start()
        elif re.search("C1", str(msg)) != None:
            self.enter_exercise(self.select_widget.ui.listWidget.item(1))
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
            client.connect(("127.0.0.1", 8082))
        except:
            print("连接超时")
        while(1):
            info = client.recv(1024)
            self._signal.emit(str(info))  # 信号发送
            info = ''

'''def listenEvent(main):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(("127.0.0.1", 8082))
    info = client.recv(1024)
    if str(info).__eq__("A"):
        main.enter_select()'''

if __name__ == '__main__':

    app = QApplication(sys.argv)
    main = MainWidget()
    # listen = QThread.moveToThread(main,)

    main.show()
    sys.exit(app.exec())





