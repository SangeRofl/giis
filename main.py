from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QPen, QTransform, QPixmap
from PyQt6.QtCore import QSize, Qt, QEvent, QTimer
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication
from model import Model
import figures

import sys

W = 821
H = 701


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.pm = QPixmap(W, H)
        self.pm.fill(QColor(255, 255, 255, 255))
        self.qp = QPainter(self.pm)
        self.mouse_cur_pos = QtCore.QPoint(-1, -1)
        self.lbl_pressed = False
        self.field_label.setPixmap(self.pm)
        self.field_label.update()
        self.model = Model(W, H)
        self.connect_signals()
        self.pix_rat = 1
        self.show()

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(1280, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.field_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.field_label.setGeometry(QtCore.QRect(450, 9, 821, 701))
        self.field_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.field_label.setText("")
        self.field_label.setIndent(-1)
        self.field_label.setObjectName("field_label")
        self.coords_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.coords_label.setGeometry(QtCore.QRect(1170, 680, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.coords_label.setFont(font)
        self.coords_label.setObjectName("coords_label")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 421, 341))
        self.tabWidget.setObjectName("tabWidget")
        self.segment_tab = QtWidgets.QWidget()
        self.segment_tab.setObjectName("segment_tab")
        self.coords_groupBox = QtWidgets.QGroupBox(parent=self.segment_tab)
        self.coords_groupBox.setGeometry(QtCore.QRect(10, 10, 271, 121))
        self.coords_groupBox.setObjectName("coords_groupBox")
        self.label_4 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_4.setGeometry(QtCore.QRect(180, 20, 47, 13))
        self.label_4.setObjectName("label_4")
        self.y2_spinBox_4 = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.y2_spinBox_4.setGeometry(QtCore.QRect(180, 90, 71, 22))
        self.y2_spinBox_4.setMinimum(1)
        self.y2_spinBox_4.setMaximum(720)
        self.y2_spinBox_4.setObjectName("y2_spinBox_4")
        self.label_5 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_5.setGeometry(QtCore.QRect(180, 68, 47, 16))
        self.label_5.setObjectName("label_5")
        self.x2_spinBox_3 = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.x2_spinBox_3.setGeometry(QtCore.QRect(180, 40, 71, 22))
        self.x2_spinBox_3.setMinimum(1)
        self.x2_spinBox_3.setMaximum(1280)
        self.x2_spinBox_3.setObjectName("x2_spinBox_3")
        self.y1_spinBox_2 = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.y1_spinBox_2.setGeometry(QtCore.QRect(20, 90, 71, 22))
        self.y1_spinBox_2.setMinimum(1)
        self.y1_spinBox_2.setMaximum(720)
        self.y1_spinBox_2.setObjectName("y1_spinBox_2")
        self.label_2 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 68, 47, 16))
        self.label_3.setObjectName("label_3")
        self.x1_spinBox = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.x1_spinBox.setGeometry(QtCore.QRect(20, 40, 71, 22))
        self.x1_spinBox.setMinimum(1)
        self.x1_spinBox.setMaximum(1280)
        self.x1_spinBox.setObjectName("x1_spinBox")
        self.algorithm_group_box = QtWidgets.QGroupBox(parent=self.segment_tab)
        self.algorithm_group_box.setGeometry(QtCore.QRect(10, 150, 221, 111))
        self.algorithm_group_box.setObjectName("algorithm_group_box")
        self.cda_radio_button = QtWidgets.QRadioButton(parent=self.algorithm_group_box)
        self.cda_radio_button.setGeometry(QtCore.QRect(10, 20, 82, 21))
        self.cda_radio_button.setChecked(True)
        self.cda_radio_button.setObjectName("cda_radio_button")
        self.brezenh_radio_button = QtWidgets.QRadioButton(parent=self.algorithm_group_box)
        self.brezenh_radio_button.setGeometry(QtCore.QRect(10, 50, 141, 21))
        self.brezenh_radio_button.setChecked(False)
        self.brezenh_radio_button.setObjectName("brezenh_radio_button")
        self.woo_radio_button = QtWidgets.QRadioButton(parent=self.algorithm_group_box)
        self.woo_radio_button.setGeometry(QtCore.QRect(10, 80, 91, 21))
        self.woo_radio_button.setObjectName("woo_radio_button")
        self.tabWidget.addTab(self.segment_tab, "")
        self.second_order_lines_tab = QtWidgets.QWidget()
        self.second_order_lines_tab.setObjectName("second_order_lines_tab")
        self.groupBox = QtWidgets.QGroupBox(parent=self.second_order_lines_tab)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.groupBox.setObjectName("groupBox")
        self.okr_radioButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.okr_radioButton.setGeometry(QtCore.QRect(10, 20, 82, 17))
        self.okr_radioButton.setChecked(True)
        self.okr_radioButton.setObjectName("okr_radioButton")
        self.ell_radioButton_2 = QtWidgets.QRadioButton(parent=self.groupBox)
        self.ell_radioButton_2.setGeometry(QtCore.QRect(10, 40, 82, 21))
        self.ell_radioButton_2.setObjectName("ell_radioButton_2")
        self.gip_radioButton_3 = QtWidgets.QRadioButton(parent=self.groupBox)
        self.gip_radioButton_3.setGeometry(QtCore.QRect(10, 60, 82, 21))
        self.gip_radioButton_3.setObjectName("gip_radioButton_3")
        self.par_radioButton_4 = QtWidgets.QRadioButton(parent=self.groupBox)
        self.par_radioButton_4.setGeometry(QtCore.QRect(10, 80, 82, 21))
        self.par_radioButton_4.setObjectName("par_radioButton_4")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 100, 341, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label_6.setObjectName("label_6")
        self.ok_x_spinBox_2 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.ok_x_spinBox_2.setGeometry(QtCore.QRect(10, 40, 71, 22))
        self.ok_x_spinBox_2.setMinimum(1)
        self.ok_x_spinBox_2.setMaximum(1280)
        self.ok_x_spinBox_2.setObjectName("ok_x_spinBox_2")
        self.ok_y_spinBox_3 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.ok_y_spinBox_3.setGeometry(QtCore.QRect(10, 100, 71, 22))
        self.ok_y_spinBox_3.setMinimum(1)
        self.ok_y_spinBox_3.setMaximum(1280)
        self.ok_y_spinBox_3.setObjectName("ok_y_spinBox_3")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 47, 13))
        self.label_7.setObjectName("label_7")
        self.ok_r_spinBox_4 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.ok_r_spinBox_4.setGeometry(QtCore.QRect(120, 40, 71, 22))
        self.ok_r_spinBox_4.setMinimum(1)
        self.ok_r_spinBox_4.setMaximum(1280)
        self.ok_r_spinBox_4.setObjectName("ok_r_spinBox_4")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(120, 20, 47, 13))
        self.label_8.setObjectName("label_8")
        self.tabWidget.addTab(self.second_order_lines_tab, "")
        self.build_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.build_button.setGeometry(QtCore.QRect(10, 690, 91, 23))
        self.build_button.setObjectName("build_button")
        self.clear_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(340, 690, 91, 23))
        self.clear_button.setObjectName("clear_button")
        self.console_textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.console_textEdit.setGeometry(QtCore.QRect(10, 350, 421, 241))
        self.console_textEdit.setObjectName("console_textEdit")
        self.debug_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.debug_groupBox.setGeometry(QtCore.QRect(10, 600, 251, 51))
        self.debug_groupBox.setObjectName("debug_groupBox")
        self.debug_cancel_button = QtWidgets.QPushButton(parent=self.debug_groupBox)
        self.debug_cancel_button.setGeometry(QtCore.QRect(170, 20, 75, 23))
        self.debug_cancel_button.setObjectName("debug_cancel_button")
        self.debug_back_button = QtWidgets.QPushButton(parent=self.debug_groupBox)
        self.debug_back_button.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.debug_back_button.setObjectName("debug_back_button")
        self.debug_next_button = QtWidgets.QPushButton(parent=self.debug_groupBox)
        self.debug_next_button.setGeometry(QtCore.QRect(90, 20, 75, 23))
        self.debug_next_button.setObjectName("debug_next_button")
        self.debug_checkBox = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.debug_checkBox.setGeometry(QtCore.QRect(110, 695, 121, 17))
        self.debug_checkBox.setObjectName("debug_checkBox")
        self.select_data_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.select_data_button.setGeometry(QtCore.QRect(10, 660, 171, 23))
        self.select_data_button.setObjectName("select_data_button")
        self.setCentralWidget(self.centralwidget)
        self.field_label.setMouseTracking(True)

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.coords_label.setText(_translate("MainWindow", "x: | y:"))
        self.coords_groupBox.setTitle(_translate("MainWindow", "Координаты концов отрезка"))
        self.label_4.setText(_translate("MainWindow", "x2"))
        self.label_5.setText(_translate("MainWindow", "y2"))
        self.label_2.setText(_translate("MainWindow", "x1"))
        self.label_3.setText(_translate("MainWindow", "y1"))
        self.algorithm_group_box.setTitle(_translate("MainWindow", "Алгоритм построения"))
        self.cda_radio_button.setText(_translate("MainWindow", "ЦДА"))
        self.brezenh_radio_button.setText(_translate("MainWindow", "алгоритм Брезенхема"))
        self.woo_radio_button.setText(_translate("MainWindow", "алгоритм Ву"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.segment_tab), _translate("MainWindow", "Отрезки"))
        self.groupBox.setTitle(_translate("MainWindow", "Вид линии"))
        self.okr_radioButton.setText(_translate("MainWindow", "Окружность"))
        self.ell_radioButton_2.setText(_translate("MainWindow", "Эллипс"))
        self.gip_radioButton_3.setText(_translate("MainWindow", "Гипербола"))
        self.par_radioButton_4.setText(_translate("MainWindow", "Парабола"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Параметры"))
        self.label_6.setText(_translate("MainWindow", "x"))
        self.label_7.setText(_translate("MainWindow", "y"))
        self.label_8.setText(_translate("MainWindow", "R"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.second_order_lines_tab),
                                  _translate("MainWindow", "Линии 2-го порядка"))
        self.build_button.setText(_translate("MainWindow", "Построить"))
        self.clear_button.setText(_translate("MainWindow", "Отчистить"))
        self.debug_groupBox.setTitle(_translate("MainWindow", "Отладка"))
        self.debug_cancel_button.setText(_translate("MainWindow", "Отмена"))
        self.debug_back_button.setText(_translate("MainWindow", "Назад"))
        self.debug_next_button.setText(_translate("MainWindow", "Далее"))
        self.debug_checkBox.setText(_translate("MainWindow", "Включить отладку"))
        self.select_data_button.setText(_translate("MainWindow", "Выбрать данные с холста"))

    def connect_signals(self):
        self.build_button.clicked.connect(self.build_graphics)
        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.field_label.wheelEvent = self.lbl_wheel_event_handler
        self.field_label.mousePressEvent = self.lbl_pressed_event_handler
        self.field_label.mouseReleaseEvent = self.lbl_released_event_handler
        self.field_label.mouseMoveEvent = self.lbl_move_event_handler
        self.clear_button.clicked.connect(self.clear_pm)
        self.debug_next_button.clicked.connect(self.debug_next_button_clicked_handler)
        self.debug_back_button.clicked.connect(self.debug_back_button_clicked_handler)
        #self.algorithm_group_box.
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.setInterval(1000)
        # self.timer.start()
        # self.field_label.paintEvent = self.field_paint_handler
        self.field_label.event = self.mouse_move_handler

    def debug_next_button_clicked_handler(self):
        self.model.debug_next()
        for message in self.model.messages:
            self.cw(message)
        self.model.messages.clear()
        self.update()

    def debug_back_button_clicked_handler(self):
        self.model.debug_prev()
        self.update()

    def build_graphics(self):
        arg_dict = dict()
        fig_cls = None
        if self.tabWidget.currentIndex() == 0:
            arg_dict['x1'] = self.x1_spinBox.value()
            arg_dict['y1'] = self.y1_spinBox_2.value()
            arg_dict['x2'] = self.x2_spinBox_3.value()
            arg_dict['y2'] = self.y2_spinBox_4.value()
            if self.cda_radio_button.isChecked():
                fig_cls = figures.SegmentCDA
            elif self.brezenh_radio_button.isChecked():
                fig_cls = figures.SegmentBrez
            elif self.woo_radio_button.isChecked():
                fig_cls = figures.SegmentCDA
        elif self.tabWidget.currentIndex() == 1:
            arg_dict['x'] = self.ok_x_spinBox_2.value()
            arg_dict['y'] = self.ok_y_spinBox_3.value()
            arg_dict['R'] = self.ok_r_spinBox_4.value()
            if self.okr_radioButton.isChecked():
                fig_cls = figures.Okr

        self.model.add_figure(fig_cls, self.debug_checkBox.isChecked(), **arg_dict)
        self.update()

    def update(self):
        self.qp.drawPixmap(0, 0, self.model.pm)
        self.field_label.setPixmap(self.pm)


    def cw(self, text: str):
        self.console_textEdit.setText(self.console_textEdit.toPlainText()+"\n"+text)

    def tab_changed(self, tab_index: int):
        print(tab_index)
        if tab_index == 0:
            self.cw("Переключено в режим отрезков")

        elif tab_index == 1:
            self.cw("Переключено в режим линий второго порядка")
        else:
            print("Unknown error")

    def lbl_wheel_event_handler(self, e):
        angle = 1 if e.angleDelta().y() > 0 else -1
        self.pix_rat += angle
        self.pm = self.pm.scaled(W*self.pix_rat, H*self.pix_rat)
        #self.pm.setDevicePixelRatio(self.pm.devicePixelRatio() - angle)
        self.field_label.setPixmap(self.pm)


    def lbl_pressed_event_handler(self, e):
        self.lbl_pressed = True

    def lbl_released_event_handler(self, e):
        self.lbl_pressed = False
        self.mouse_cur_pos = QtCore.QPoint(-1, -1)

    def lbl_move_event_handler(self, e):
        if e.pos().x() > 0 and e.pos().y() > 0 and self.mouse_cur_pos.x() > 0 and self.mouse_cur_pos.y() > 0 and self.lbl_pressed:
            pos = e.pos() - self.mouse_cur_pos
            self.pm.scroll(pos.x(), pos.y(), self.pm.rect())
            #print(e.pos()-self.mouse_cur_pos)
            self.field_label.setPixmap(self.pm)
        self.coords_label.setText(f"x: {e.pos().x()} | y: {self.field_label.height()-e.pos().y()-1}")
        self.mouse_cur_pos = e.pos()
            # self.field_label.move(e.pos()-e.oldPos())

    def clear_pm(self):
        self.pm.fill(QColor(255, 255, 255, 255))
        self.field_label.setPixmap(self.pm)

    def mouse_move_handler(self, e):
        print(1)
        if e.type() == QEvent.Type.MouseMove:
            print(1)
        return super().event(e)

    def field_paint_handler(self, e):
        self.field_label.setPixmap(self.pm)


app = QApplication(sys.argv)
mw = MainWindow()
app.exec()