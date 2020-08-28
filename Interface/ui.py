import start
import exercise
import select
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Start(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = start.Ui_Form()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.widget = [self.ui.button_exercise, self.ui.button_history, self.ui.button_setting]


class Exercise(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = exercise.Ui_Form()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)



class Select(QWidget):

    movement = ["哑铃弯举", "哑铃侧平举", "斯科特举", "哑铃侧屈体", "深蹲"]

    def __init__(self):
        super().__init__()
        self.ui = select.Ui_Form()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        for i in self.movement:
            item = QListWidgetItem()
            item.setText(i)
            item.setSizeHint(QSize(100, 100))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.listWidget.addItem(item)

