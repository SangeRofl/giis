from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt6.QtCore import Qt
from figures import SegmentCDA
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(821, 701)
        self.lbl = QLabel()
        self.setCentralWidget(self.lbl)
        self.draw()
        self.show()

    def draw(self):
        # self.pm1 = QPixmap(300, 300)
        # self.pm1.fill(QColor(200,200,200,255))
        # self.pm2 = QPixmap(300, 300)
        # self.pm2.fill(QColor(0,0,0,0))
        # qp2 = QPainter(self.pm2)
        # qp2.setPen(QPen(QColor(0,0,0,255), 1))
        # qp2.drawLine(20, 20, 50, 50)
        # qp2.drawPoint(20,149)
        # qp1 = QPainter(self.pm1)
        # qp1.drawPixmap(0,0, self.pm2)
        # self.pm3 = QPixmap(300, 300)
        # self.pm3.fill(QColor(0,0,0,0))
        # qp3 = QPainter(self.pm3)
        # qp3.setPen(QPen(QColor(0, 0, 0, 255), 3))
        # qp3.drawLine(20, 50, 50, 20)
        # qp1.drawPixmap(0, 0, self.pm3)
        # self.pm1 = self.pm1.scaled(300, 300, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        # self.lbl.setPixmap(self.pm1)
        self.pm1 = QPixmap(100, 100)
        self.pm1.fill(QColor("red"))
        self.sw = 400
        self.sh = 400
        self.spm = QPixmap(self.sw, self.sh)
        self.spm.fill(QColor("white"))
        self.p = QPainter(self.spm)
        self.p.drawPixmap(0, 0, self.pm1)
        self.p.setPen(QPen(QColor(0,0,0,255), 1))
        self.p.drawLine(30, 0 , 80, 200)
        self.line = SegmentCDA(0, 0, 249, 249, 400, 400)
        self.line.draw()
        self.p.drawPixmap(0,0,self.line.pm)
        self.spm2 = self.spm.scaled(3200, 3200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.p2 = QPainter(self.spm2)
        self.p2.setPen(QPen(QColor(0, 0, 0, 255), 1))
        for i in range(400):
            self.p2.drawLine(i*8, 0, i*8, 7999)
            self.p2.drawLine(0, i * 8, 7999, i * 8)
        self.lbl.setPixmap(self.spm2)
        # del self.spm

    def mousePressEvent(self, a0):
        self.line.next_draw_step()
        self.p2.drawPixmap(0, 0, self.line.pm)
        self.lbl.setPixmap(self.spm2)



app = QApplication(sys.argv)
mw = MainWindow()
app.exec()