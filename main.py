from PySide2.QtWidgets import *
import sys
import numpy as np
import matplotlib.pyplot as plt
import re
from PySide2.QtGui import QIcon


class mainwindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("拟合模拟器")
        self.setFixedSize(300, 600)

        self.xlabel = QLabel("x轴", self)
        self.xlabel.move(5, 10)

        self.xedit = QTextEdit(self)
        self.xedit.move(15, 30)
        self.xedit.setPlaceholderText("示例：1,2,3,4")

        self.ylabel = QLabel("y轴", self)
        self.ylabel.move(5, 230)

        self.yedit = QTextEdit(self)
        self.yedit.move(15, 260)
        self.yedit.setPlaceholderText("示例：1,2,3,4")

        self.label = QLabel("阶次", self)
        self.label.move(5, 470)

        self.spinbox = QSpinBox(self)
        self.spinbox.move(50, 466)

        self.label2 = QLabel("步长:", self)
        self.label2.move(150, 470)

        self.spinbox2 = QSpinBox(self)
        self.spinbox2.move(190, 466)
        self.spinbox2.resize(60, 20)

        self.btn = QPushButton("拟合", self)
        self.btn.move(5, 500)
        self.btn.resize(290, 30)
        self.btn.clicked.connect(self.fitting)

        self.fedit = QTextEdit(self)
        self.fedit.move(15, 535)
        self.fedit.resize(260, 60)

    def getinfo(self):

        x = self.xedit.toPlainText()
        y = self.yedit.toPlainText()
        j = self.spinbox.value()
        b = self.spinbox2.value()

        xlist = re.split(',|，', x)
        ylist = re.split(',|，', y)
        if len(xlist) == len(ylist):
            if len(xlist) != 1:
                return xlist, ylist, j, b
            else:
                QMessageBox.information(self, "警告", "数据长度不能为空或1")
        else:
            QMessageBox.information(self, "警告", "X拟合数据与Y轴拟合数据不匹配")

    def fitting(self):

        replay = QMessageBox.information(
            self, "消息", "拟合", QMessageBox.Yes | QMessageBox.No)

        if replay == QMessageBox.Yes:

            # print(self.getinfo()[0])
            # print(self.getinfo()[1])
            # print(self.getinfo()[2])

            xmap = list(map(lambda x: float(x), self.getinfo()[0]))
            ymap = list(map(lambda y: float(y), self.getinfo()[1]))
            j = self.getinfo()[2]
            b = self.getinfo()[3]

            x = np.array(xmap)
            y = np.array(ymap)

            f = np.polyfit(x, y, j)
            p = np.poly1d(f)

            self.fedit.setText(str(p))
            if b == 0:
                yfiting = p(x)

                polt1 = plt.plot(x, y, "*", label="original")
                polt2 = plt.plot(x, yfiting, label="fitting")

                plt.legend(loc=4)
                plt.show()

            else:

                x1 = np.linspace(xmap[0], xmap[-1], b)
                yfiting = p(x1)
                polt1 = plt.plot(x, y, "*", label="original")
                polt2 = plt.plot(x1, yfiting, label="fitting")
                plt.legend(loc=4)
                plt.show()

        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./b9.ico"))
    window = mainwindow()
    window.show()
    sys.exit(app.exec_())
