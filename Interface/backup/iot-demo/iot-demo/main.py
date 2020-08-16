import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ui


class MainWidget(QWidget):

    ANGLE = 1
    MUSCLE_STRENGTH = 2
    PHYSIOLOGICAL_FUNCTION = 3
    NUMBER = 4
    HINT = 5

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
        if i == self.ANGLE:
            self.exercise_widget.ui.angle.setText(text)
        elif i == self.MUSCLE_STRENGTH:
            self.exercise_widget.ui.muscleStrength.setText(text)
        elif i == self.PHYSIOLOGICAL_FUNCTION:
            self.exercise_widget.ui.physiologicalFunction.setText(text)
        elif i == self.NUMBER:
            self.exercise_widget.ui.number.setText(text)
        elif i == self.HINT:
            self.exercise_widget.ui.hint.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    sys.exit(app.exec())





