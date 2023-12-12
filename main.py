# Линкевич Александр Васильевич, группа 021701
# 24.11.2023
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QFont, QBrush, QPen, QTransform, QPixmap
from PyQt6.QtCore import QSize, Qt, QEvent, QTimer
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QApplication
from model import Model
import figures
import time


import sys

W = 600
H = 600


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.pm = QPixmap(W, H)
        self.real_pm = QPixmap(W, H)
        self.real_qp = QPainter(self.real_pm)
        self.pm.fill(QColor(255, 255, 255, 255))
        self.qp = QPainter(self.pm)
        self.pm_cur_pos = QtCore.QPoint(0, 0)
        self.mouse_cur_pos = QtCore.QPoint(-1, -1)
        self.lbl_pressed = False
        self.field_label.update()
        self.model = Model(W, H)
        self.connect_signals()
        self.pix_rat = 1
        self.field_data_select_mode = False
        self.data_to_select_count = -1
        self.data_from_field = []
        self.timers_init()
        self.update()
        self.show()

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(1059, 624)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.field_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.field_label.setGeometry(QtCore.QRect(450, 9, 600, 600))
        self.field_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.field_label.setText("")
        self.field_label.setIndent(-1)
        self.field_label.setObjectName("field_label")
        self.coords_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.coords_label.setGeometry(QtCore.QRect(930, 580, 121, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(99)
        self.coords_label.setFont(font)
        self.coords_label.setStyleSheet("font-weight: 1000;")
        self.coords_label.setObjectName("coords_label")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 421, 291))
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
        self.y2_spinBox_4.setMinimum(-1000)
        self.y2_spinBox_4.setMaximum(1000)
        self.y2_spinBox_4.setObjectName("y2_spinBox_4")
        self.label_5 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_5.setGeometry(QtCore.QRect(180, 68, 47, 16))
        self.label_5.setObjectName("label_5")
        self.x2_spinBox_3 = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.x2_spinBox_3.setGeometry(QtCore.QRect(180, 40, 71, 22))
        self.x2_spinBox_3.setMinimum(-1000)
        self.x2_spinBox_3.setMaximum(1000)
        self.x2_spinBox_3.setObjectName("x2_spinBox_3")
        self.y1_spinBox_2 = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.y1_spinBox_2.setGeometry(QtCore.QRect(20, 90, 71, 22))
        self.y1_spinBox_2.setMinimum(-1000)
        self.y1_spinBox_2.setMaximum(1000)
        self.y1_spinBox_2.setObjectName("y1_spinBox_2")
        self.label_2 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.coords_groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 68, 47, 16))
        self.label_3.setObjectName("label_3")
        self.x1_spinBox = QtWidgets.QSpinBox(parent=self.coords_groupBox)
        self.x1_spinBox.setGeometry(QtCore.QRect(20, 40, 71, 22))
        self.x1_spinBox.setMinimum(-1000)
        self.x1_spinBox.setMaximum(1000)
        self.x1_spinBox.setObjectName("x1_spinBox")
        self.algorithm_group_box = QtWidgets.QGroupBox(parent=self.segment_tab)
        self.algorithm_group_box.setGeometry(QtCore.QRect(10, 150, 221, 111))
        self.algorithm_group_box.setObjectName("algorithm_group_box")
        self.cda_radio_button = QtWidgets.QRadioButton(parent=self.algorithm_group_box)
        self.cda_radio_button.setGeometry(QtCore.QRect(10, 20, 171, 21))
        self.cda_radio_button.setChecked(True)
        self.cda_radio_button.setObjectName("cda_radio_button")
        self.brezenh_radio_button = QtWidgets.QRadioButton(parent=self.algorithm_group_box)
        self.brezenh_radio_button.setGeometry(QtCore.QRect(10, 50, 201, 21))
        self.brezenh_radio_button.setChecked(False)
        self.brezenh_radio_button.setObjectName("brezenh_radio_button")
        self.woo_radio_button = QtWidgets.QRadioButton(parent=self.algorithm_group_box)
        self.woo_radio_button.setGeometry(QtCore.QRect(10, 80, 211, 21))
        self.woo_radio_button.setObjectName("woo_radio_button")
        self.tabWidget.addTab(self.segment_tab, "")
        self.second_order_lines_tab = QtWidgets.QWidget()
        self.second_order_lines_tab.setObjectName("second_order_lines_tab")
        self.groupBox = QtWidgets.QGroupBox(parent=self.second_order_lines_tab)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 361, 251))
        self.groupBox.setObjectName("groupBox")
        self.okr_radioButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.okr_radioButton.setGeometry(QtCore.QRect(10, 20, 201, 17))
        self.okr_radioButton.setChecked(True)
        self.okr_radioButton.setObjectName("okr_radioButton")
        self.ell_radioButton_2 = QtWidgets.QRadioButton(parent=self.groupBox)
        self.ell_radioButton_2.setGeometry(QtCore.QRect(10, 40, 181, 21))
        self.ell_radioButton_2.setObjectName("ell_radioButton_2")
        self.gip_radioButton_3 = QtWidgets.QRadioButton(parent=self.groupBox)
        self.gip_radioButton_3.setGeometry(QtCore.QRect(10, 60, 171, 21))
        self.gip_radioButton_3.setObjectName("gip_radioButton_3")
        self.par_radioButton_4 = QtWidgets.QRadioButton(parent=self.groupBox)
        self.par_radioButton_4.setGeometry(QtCore.QRect(10, 80, 181, 21))
        self.par_radioButton_4.setObjectName("par_radioButton_4")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 100, 341, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.label_6.setObjectName("label_6")
        self.sec_line_spinBox_1 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.sec_line_spinBox_1.setGeometry(QtCore.QRect(10, 40, 71, 22))
        self.sec_line_spinBox_1.setMinimum(-1000)
        self.sec_line_spinBox_1.setMaximum(1000)
        self.sec_line_spinBox_1.setObjectName("sec_line_spinBox_1")
        self.sec_line_spinBox_2 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.sec_line_spinBox_2.setGeometry(QtCore.QRect(10, 100, 71, 22))
        self.sec_line_spinBox_2.setMinimum(-1000)
        self.sec_line_spinBox_2.setMaximum(1000)
        self.sec_line_spinBox_2.setProperty("value", 1)
        self.sec_line_spinBox_2.setObjectName("sec_line_spinBox_2")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 111, 16))
        self.label_7.setObjectName("label_7")
        self.sec_line_spinBox_3 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.sec_line_spinBox_3.setGeometry(QtCore.QRect(160, 40, 71, 22))
        self.sec_line_spinBox_3.setMinimum(-1000)
        self.sec_line_spinBox_3.setMaximum(1000)
        self.sec_line_spinBox_3.setObjectName("sec_line_spinBox_3")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(160, 20, 131, 16))
        self.label_8.setObjectName("label_8")
        self.sec_line_spinBox_4 = QtWidgets.QSpinBox(parent=self.groupBox_2)
        self.sec_line_spinBox_4.setGeometry(QtCore.QRect(160, 100, 71, 22))
        self.sec_line_spinBox_4.setMinimum(-1000)
        self.sec_line_spinBox_4.setMaximum(1000)
        self.sec_line_spinBox_4.setObjectName("sec_line_spinBox_4")
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(160, 80, 121, 16))
        self.label_9.setObjectName("label_9")
        self.tabWidget.addTab(self.second_order_lines_tab, "")
        self.par_line_tab = QtWidgets.QWidget()
        self.par_line_tab.setObjectName("par_line_tab")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.par_line_tab)
        self.groupBox_3.setGeometry(QtCore.QRect(19, 9, 381, 241))
        self.groupBox_3.setObjectName("groupBox_3")
        self.ermit_radioButton = QtWidgets.QRadioButton(parent=self.groupBox_3)
        self.ermit_radioButton.setGeometry(QtCore.QRect(10, 20, 181, 21))
        self.ermit_radioButton.setChecked(True)
        self.ermit_radioButton.setObjectName("ermit_radioButton")
        self.bez_radioButton = QtWidgets.QRadioButton(parent=self.groupBox_3)
        self.bez_radioButton.setGeometry(QtCore.QRect(10, 40, 161, 21))
        self.bez_radioButton.setObjectName("bez_radioButton")
        self.b_splain_radioButton = QtWidgets.QRadioButton(parent=self.groupBox_3)
        self.b_splain_radioButton.setGeometry(QtCore.QRect(10, 60, 141, 21))
        self.b_splain_radioButton.setObjectName("b_splain_radioButton")
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.groupBox_3)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 90, 361, 141))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_10 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.label_10.setObjectName("label_10")
        self.par_line_spinBox_5 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_5.setGeometry(QtCore.QRect(10, 40, 71, 22))
        self.par_line_spinBox_5.setMinimum(-1000)
        self.par_line_spinBox_5.setMaximum(1000)
        self.par_line_spinBox_5.setObjectName("par_line_spinBox_5")
        self.par_line_spinBox_6 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_6.setGeometry(QtCore.QRect(10, 90, 71, 22))
        self.par_line_spinBox_6.setMinimum(-1000)
        self.par_line_spinBox_6.setMaximum(1000)
        self.par_line_spinBox_6.setObjectName("par_line_spinBox_6")
        self.label_11 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(10, 70, 111, 16))
        self.label_11.setObjectName("label_11")
        self.par_line_spinBox_7 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_7.setGeometry(QtCore.QRect(90, 40, 71, 22))
        self.par_line_spinBox_7.setMinimum(-1000)
        self.par_line_spinBox_7.setMaximum(1000)
        self.par_line_spinBox_7.setObjectName("par_line_spinBox_7")
        self.label_12 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(90, 20, 111, 16))
        self.label_12.setObjectName("label_12")
        self.par_line_spinBox_8 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_8.setGeometry(QtCore.QRect(90, 90, 71, 22))
        self.par_line_spinBox_8.setMinimum(-1000)
        self.par_line_spinBox_8.setMaximum(1000)
        self.par_line_spinBox_8.setObjectName("par_line_spinBox_8")
        self.label_13 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(90, 70, 111, 16))
        self.label_13.setObjectName("label_13")
        self.par_line_spinBox_9 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_9.setGeometry(QtCore.QRect(170, 40, 71, 22))
        self.par_line_spinBox_9.setMinimum(-1000)
        self.par_line_spinBox_9.setMaximum(1000)
        self.par_line_spinBox_9.setObjectName("par_line_spinBox_9")
        self.label_14 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_14.setGeometry(QtCore.QRect(170, 20, 111, 16))
        self.label_14.setObjectName("label_14")
        self.par_line_spinBox_10 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_10.setGeometry(QtCore.QRect(170, 90, 71, 22))
        self.par_line_spinBox_10.setMinimum(-1000)
        self.par_line_spinBox_10.setMaximum(1000)
        self.par_line_spinBox_10.setObjectName("par_line_spinBox_10")
        self.label_15 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_15.setGeometry(QtCore.QRect(170, 70, 111, 16))
        self.label_15.setObjectName("label_15")
        self.par_line_spinBox_11 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_11.setGeometry(QtCore.QRect(250, 40, 71, 22))
        self.par_line_spinBox_11.setMinimum(-1000)
        self.par_line_spinBox_11.setMaximum(1000)
        self.par_line_spinBox_11.setObjectName("par_line_spinBox_11")
        self.label_16 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(250, 20, 111, 16))
        self.label_16.setObjectName("label_16")
        self.par_line_spinBox_12 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.par_line_spinBox_12.setGeometry(QtCore.QRect(250, 90, 71, 22))
        self.par_line_spinBox_12.setMinimum(-1000)
        self.par_line_spinBox_12.setMaximum(1000)
        self.par_line_spinBox_12.setObjectName("par_line_spinBox_12")
        self.label_17 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_17.setGeometry(QtCore.QRect(250, 70, 111, 16))
        self.label_17.setObjectName("label_17")
        self.spline_checkBox = QtWidgets.QCheckBox(parent=self.groupBox_4)
        self.spline_checkBox.setGeometry(QtCore.QRect(10, 120, 191, 17))
        self.spline_checkBox.setObjectName("spline_checkBox")
        self.tabWidget.addTab(self.par_line_tab, "")
        self.build_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.build_button.setGeometry(QtCore.QRect(20, 595, 91, 23))
        self.build_button.setObjectName("build_button")
        self.clear_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clear_button.setGeometry(QtCore.QRect(280, 595, 91, 23))
        self.clear_button.setObjectName("clear_button")
        self.console_textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.console_textEdit.setGeometry(QtCore.QRect(10, 300, 421, 231))
        self.console_textEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.console_textEdit.setReadOnly(True)
        self.console_textEdit.setObjectName("console_textEdit")
        self.debug_groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.debug_groupBox.setGeometry(QtCore.QRect(10, 540, 251, 51))
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
        self.debug_checkBox.setGeometry(QtCore.QRect(120, 600, 121, 17))
        self.debug_checkBox.setObjectName("debug_checkBox")
        self.select_data_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.select_data_button.setGeometry(QtCore.QRect(270, 560, 171, 23))
        self.select_data_button.setObjectName("select_data_button")
        self.zoom_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.zoom_label.setGeometry(QtCore.QRect(460, 580, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(99)
        self.zoom_label.setFont(font)
        self.zoom_label.setStyleSheet("font-weight: 1000;")
        self.zoom_label.setObjectName("zoom_label")
        self.setCentralWidget(self.centralwidget)
        self.field_label.setMouseTracking(True)
        self.label_9.setVisible(False)
        self.sec_line_spinBox_4.setVisible(False)
        self.spline_checkBox.setVisible(False)

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
        self.label_9.setText(_translate("MainWindow", "R"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.second_order_lines_tab),
                                  _translate("MainWindow", "Линии 2-го порядка"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Кривая"))
        self.ermit_radioButton.setText(_translate("MainWindow", "форма Эрмита"))
        self.bez_radioButton.setText(_translate("MainWindow", "форма Безье"))
        self.b_splain_radioButton.setText(_translate("MainWindow", "В-сплайн"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Параметры"))
        self.label_10.setText(_translate("MainWindow", "P1x"))
        self.label_11.setText(_translate("MainWindow", "P1y"))
        self.label_12.setText(_translate("MainWindow", "P4x"))
        self.label_13.setText(_translate("MainWindow", "P4y"))
        self.label_14.setText(_translate("MainWindow", "R1x"))
        self.label_15.setText(_translate("MainWindow", "R1y"))
        self.label_16.setText(_translate("MainWindow", "R4x"))
        self.label_17.setText(_translate("MainWindow", "R4y"))
        self.spline_checkBox.setText(_translate("MainWindow", "Замкнутый"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.par_line_tab),
                                  _translate("MainWindow", "Параметрические кривые"))
        self.build_button.setText(_translate("MainWindow", "Построить"))
        self.clear_button.setText(_translate("MainWindow", "Отчистить"))
        self.debug_groupBox.setTitle(_translate("MainWindow", "Отладка"))
        self.debug_cancel_button.setText(_translate("MainWindow", "Отмена"))
        self.debug_back_button.setText(_translate("MainWindow", "Назад"))
        self.debug_next_button.setText(_translate("MainWindow", "Далее"))
        self.debug_checkBox.setText(_translate("MainWindow", "Включить отладку"))
        self.select_data_button.setText(_translate("MainWindow", "Выбрать данные с холста"))
        self.zoom_label.setText(_translate("MainWindow", "zoom:"))

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
        self.select_data_button.clicked.connect(self.select_data_button_clicked_handler)
        self.okr_radioButton.toggled.connect(self.okr_radioButton_toggled_handler)
        self.ell_radioButton_2.toggled.connect(self.ell_radioButton_toggled_handler)
        self.gip_radioButton_3.toggled.connect(self.ell_radioButton_toggled_handler)
        self.par_radioButton_4.toggled.connect(self.par_radioButton_toggled_handler)
        self.ermit_radioButton.toggled.connect(self.ermit_radioButton_toggled_handler)
        self.bez_radioButton.toggled.connect(self.bez_radioButton_toggled_handler)
        self.b_splain_radioButton.toggled.connect(self.b_splain_radioButton_toggled_handler)
        #self.algorithm_group_box.
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.setInterval(1000)
        # self.timer.start()
        # self.field_label.paintEvent = self.field_paint_handler
        self.field_label.event = self.mouse_move_handler

    def timers_init(self):
        self.field_click_time = 0
        self.field_click_start = 0

    def debug_next_button_clicked_handler(self):
        self.model.debug_next()
        for message in self.model.messages:
            self.cw(message)
        self.model.messages.clear()
        self.update()

    def debug_back_button_clicked_handler(self):
        self.model.debug_prev()
        self.update()

    def select_data_button_clicked_handler(self):
        if self.field_data_select_mode == False:
            self.select_data_button.setText("Отмена")
            if self.tabWidget.currentIndex() == 0:
                self.get_data_from_field(2)
            elif self.tabWidget.currentIndex() == 1:
                if self.okr_radioButton.isChecked():
                    self.get_data_from_field(2)
                elif self.ell_radioButton_2.isChecked():
                    self.get_data_from_field(2)
                elif self.gip_radioButton_3.isChecked():
                    self.get_data_from_field(2)
                elif self.par_radioButton_4.isChecked():
                    self.get_data_from_field(2)
                else:
                    print("Unknown radio")
            elif self.tabWidget.currentIndex() == 2:
                self.get_data_from_field(4)
            else:
                print("Unknown tab")
        else:
            self.select_data_button.setText("Выбрать данные с холста")
            self.field_data_select_mode = False
            self.data_from_field.clear()
            self.data_to_select_count = 0

    def okr_radioButton_toggled_handler(self, status):
        if status:
            self.label_6.setText("x")
            self.label_7.setText("y")
            self.label_8.setText("R")
            self.label_9.setVisible(False)
            self.sec_line_spinBox_4.setVisible(False)

    def ell_radioButton_toggled_handler(self, status):
        if status:
            self.label_6.setText("x")
            self.label_7.setText("y")
            self.label_8.setText("a")
            self.label_9.setText("b")
            self.label_9.setVisible(True)
            self.sec_line_spinBox_4.setVisible(True)

    def par_radioButton_toggled_handler(self, status):
        if status:
            self.okr_radioButton_toggled_handler(True)
            self.label_8.setText("p")

    def ermit_radioButton_toggled_handler(self, status):
        if status:
            self.label_10.setText("P1x")
            self.label_11.setText("P1y")
            self.label_12.setText("P4x")
            self.label_13.setText("P4y")
            self.label_14.setText("R1x")
            self.label_15.setText("R1y")
            self.label_16.setText("R4x")
            self.label_17.setText("R4y")
            self.spline_checkBox.setVisible(False)

    def bez_radioButton_toggled_handler(self, status):
        if status:
            self.label_10.setText("P1x")
            self.label_11.setText("P1y")
            self.label_12.setText("P2x")
            self.label_13.setText("P2y")
            self.label_14.setText("P3x")
            self.label_15.setText("P3y")
            self.label_16.setText("P4x")
            self.label_17.setText("P4y")
            self.spline_checkBox.setVisible(False)

    def b_splain_radioButton_toggled_handler(self, status):
        if status:
            self.label_10.setText("P1x")
            self.label_11.setText("P1y")
            self.label_12.setText("P2x")
            self.label_13.setText("P2y")
            self.label_14.setText("P3x")
            self.label_15.setText("P3y")
            self.label_16.setText("P4x")
            self.label_17.setText("P4y")
            self.spline_checkBox.setVisible(True)

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
                fig_cls = figures.SegmentWoo
        elif self.tabWidget.currentIndex() == 1:
            if self.okr_radioButton.isChecked():
                arg_dict['x'] = self.sec_line_spinBox_1.value()
                arg_dict['y'] = self.sec_line_spinBox_2.value()
                arg_dict['R'] = self.sec_line_spinBox_3.value()
                fig_cls = figures.Okr
            elif self.ell_radioButton_2.isChecked():
                arg_dict['x'] = self.sec_line_spinBox_1.value()
                arg_dict['y'] = self.sec_line_spinBox_2.value()
                arg_dict['a'] = self.sec_line_spinBox_3.value()
                arg_dict['b'] = self.sec_line_spinBox_4.value()
                fig_cls = figures.Ellipse
            elif self.gip_radioButton_3.isChecked():
                arg_dict['x'] = self.sec_line_spinBox_1.value()
                arg_dict['y'] = self.sec_line_spinBox_2.value()
                arg_dict['a'] = self.sec_line_spinBox_3.value()
                arg_dict['b'] = self.sec_line_spinBox_4.value()
                fig_cls = figures.Gip
            elif self.par_radioButton_4.isChecked():
                arg_dict['x'] = self.sec_line_spinBox_1.value()
                arg_dict['y'] = self.sec_line_spinBox_2.value()
                arg_dict['p'] = self.sec_line_spinBox_3.value()
                fig_cls = figures.Par
        elif self.tabWidget.currentIndex() == 2:
            if self.ermit_radioButton.isChecked():
                arg_dict['p1x'] = self.par_line_spinBox_5.value()
                arg_dict['p1y'] = self.par_line_spinBox_6.value()
                arg_dict['p4x'] = self.par_line_spinBox_7.value()
                arg_dict['p4y'] = self.par_line_spinBox_8.value()
                arg_dict['r1x'] = self.par_line_spinBox_9.value()
                arg_dict['r1y'] = self.par_line_spinBox_10.value()
                arg_dict['r4x'] = self.par_line_spinBox_11.value()
                arg_dict['r4y'] = self.par_line_spinBox_12.value()
                fig_cls = figures.ErmitInterpol
            elif self.bez_radioButton.isChecked():
                arg_dict['p1x'] = self.par_line_spinBox_5.value()
                arg_dict['p1y'] = self.par_line_spinBox_6.value()
                arg_dict['p2x'] = self.par_line_spinBox_7.value()
                arg_dict['p2y'] = self.par_line_spinBox_8.value()
                arg_dict['p3x'] = self.par_line_spinBox_9.value()
                arg_dict['p3y'] = self.par_line_spinBox_10.value()
                arg_dict['p4x'] = self.par_line_spinBox_11.value()
                arg_dict['p4y'] = self.par_line_spinBox_12.value()
                fig_cls = figures.BezInterpol
            elif self.b_splain_radioButton.isChecked():
                arg_dict['points'] = [
                    (self.par_line_spinBox_5.value(), self.par_line_spinBox_6.value()),
                    (self.par_line_spinBox_7.value(), self.par_line_spinBox_8.value()),
                    (self.par_line_spinBox_9.value(), self.par_line_spinBox_10.value()),
                    (self.par_line_spinBox_11.value(), self.par_line_spinBox_12.value()),

                ]
                arg_dict['closed'] = True if self.spline_checkBox.isChecked() else False
                fig_cls = figures.SplineInterpol

        self.model.add_figure(fig_cls, self.debug_checkBox.isChecked(), **arg_dict)
        self.update()

    def update(self):
        self.pm.fill(QColor(255,255,255,255))
        self.qp.drawPixmap(self.pm_cur_pos.x(), self.pm_cur_pos.y(), self.model.pm)
        cropped = self.pm.copy(0, 0, W // self.pix_rat, H // self.pix_rat)
        scaled = cropped.scaled(W, H)
        self.real_qp.drawPixmap(0, 0, scaled)
        self.real_qp.drawLine((self.pm_cur_pos.x()-1)*self.pix_rat,
                              (self.pm_cur_pos.y()+H+1)*self.pix_rat,
                              (self.pm_cur_pos.x()+W+1)*self.pix_rat,
                              (self.pm_cur_pos.y()+H+1)*self.pix_rat)
        self.real_qp.drawLine((self.pm_cur_pos.x() - 1) * self.pix_rat,
                              (self.pm_cur_pos.y() - 1) * self.pix_rat,
                              (self.pm_cur_pos.x() - 1) * self.pix_rat,
                              (self.pm_cur_pos.y() + H + 1) * self.pix_rat)
        self.real_qp.drawLine((self.pm_cur_pos.x() - 1) * self.pix_rat,
                              (self.pm_cur_pos.y() - 1) * self.pix_rat,
                              (self.pm_cur_pos.x() + W + 1) * self.pix_rat,
                              (self.pm_cur_pos.y() - 1) * self.pix_rat)
        self.real_qp.drawLine((self.pm_cur_pos.x() + W + 1) * self.pix_rat,
                              (self.pm_cur_pos.y() - 1) * self.pix_rat,
                              (self.pm_cur_pos.x() + W + 1) * self.pix_rat,
                              (self.pm_cur_pos.y() + H + 1) * self.pix_rat)
        if self.pix_rat >= 10:
            self.real_qp.setPen(QPen(QColor(0, 0, 0, 155), 1))
            for i in range(0, W+1):
                self.real_qp.drawLine(self.pm_cur_pos.x() * self.pix_rat + i * self.pix_rat,
                                      self.pm_cur_pos.y() * self.pix_rat + 0,
                                      self.pm_cur_pos.x() * self.pix_rat + self.pix_rat * i,
                                      self.pm_cur_pos.y() * self.pix_rat + H * self.pix_rat)
            for i in range(0, H+1):
                self.real_qp.drawLine(self.pm_cur_pos.x() * self.pix_rat + 0,
                                      self.pm_cur_pos.y() * self.pix_rat + i * self.pix_rat,
                                      self.pm_cur_pos.x() * self.pix_rat + W * self.pix_rat,
                                      self.pm_cur_pos.y() * self.pix_rat + self.pix_rat * i)
        self.field_label.setPixmap(self.real_pm)

    def cw(self, text: str):
        self.console_textEdit.append(text)
        self.console_textEdit.ensureCursorVisible()

    def tab_changed(self, tab_index: int):
        print(tab_index)
        if tab_index == 0:
            self.cw("Переключено в режим отрезков")

        elif tab_index == 1:
            self.cw("Переключено в режим линий второго порядка")
        elif tab_index == 2:
            self.cw("Переключено в режим параметрических кривых")
        else:
            print("Unknown error")

    def lbl_wheel_event_handler(self, e):
        angle = 1 if e.angleDelta().y() > 0 else -1
        if not(angle < 0 and self.pix_rat <= 1):
            if not ((self.pix_rat == W or self.pix_rat == H) and angle > 0):
                self.pix_rat += angle
            while (W / self.pix_rat - W // self.pix_rat != 0 and H / self.pix_rat - H // self.pix_rat != 0):
                self.pix_rat += angle
        self.zoom_label.setText(f"zoom: {self.pix_rat}")
        self.update()
        #self.pm.setDevicePixelRatio(self.pm.devicePixelRatio() - angle)
        #self.field_label.setPixmap(self.pm)

    def get_data_from_field(self, points_count: int):
        self.field_data_select_mode = True
        self.data_to_select_count = points_count


    def lbl_pressed_event_handler(self, e):
        self.lbl_pressed = True
        self.field_click_start = time.time()

    def lbl_released_event_handler(self, e):
        self.lbl_pressed = False
        self.mouse_cur_pos = QtCore.QPoint(-1, -1)
        field_click_end = time.time()
        self.field_click_time = field_click_end - self.field_click_start
        if self.field_data_select_mode == True and self.field_click_time <= 0.1:
            x = e.pos().x() // self.pix_rat - self.pm_cur_pos.x()
            y = H - (e.pos().y() // self.pix_rat - self.pm_cur_pos.y()) - 1
            print(x, y)
            self.data_from_field.append(QtCore.QPoint(x, y))
            self.data_to_select_count -= 1
            self.cw(f"Точка выбрана. Осталось выбрать еще {self.data_to_select_count}")
            if self.data_to_select_count <= 0:
                self.field_data_select_mode = False
                self.select_data_button.setText("Выбрать данные с холста")
                self.cw(f"Выбор точек завершен")
                self.build_from_field()

    def build_from_field(self):
        if self.tabWidget.currentIndex() == 0:
            self.x1_spinBox.setValue(self.data_from_field[0].x())
            self.y1_spinBox_2.setValue(self.data_from_field[0].y())
            self.x2_spinBox_3.setValue(self.data_from_field[1].x())
            self.y2_spinBox_4.setValue(self.data_from_field[1].y())
        elif self.tabWidget.currentIndex() == 1:
            if self.okr_radioButton.isChecked():
                self.sec_line_spinBox_1.setValue(self.data_from_field[0].x())
                self.sec_line_spinBox_2.setValue(self.data_from_field[0].y())
                self.sec_line_spinBox_3.setValue(int(((self.data_from_field[0].x() - self.data_from_field[1].x())**2+(self.data_from_field[0].y() - self.data_from_field[1].y())**2)**0.5))
            elif self.ell_radioButton_2.isChecked():
                self.sec_line_spinBox_1.setValue(self.data_from_field[0].x())
                self.sec_line_spinBox_2.setValue(self.data_from_field[0].y())
                self.sec_line_spinBox_3.setValue(self.data_from_field[1].x() - self.data_from_field[0].x())
                self.sec_line_spinBox_4.setValue(self.data_from_field[1].y() - self.data_from_field[0].y())
            elif self.gip_radioButton_3.isChecked():
                self.sec_line_spinBox_1.setValue(self.data_from_field[0].x())
                self.sec_line_spinBox_2.setValue(self.data_from_field[0].y())
                self.sec_line_spinBox_3.setValue(self.data_from_field[1].x() - self.data_from_field[0].x())
                self.sec_line_spinBox_4.setValue(self.data_from_field[1].y() - self.data_from_field[0].y())
            elif self.par_radioButton_4.isChecked():
                self.sec_line_spinBox_1.setValue(self.data_from_field[0].x())
                self.sec_line_spinBox_2.setValue(self.data_from_field[0].y())
                self.sec_line_spinBox_3.setValue(self.data_from_field[1].x() - self.data_from_field[0].x())
        elif self.tabWidget.currentIndex() == 2:
            if self.ermit_radioButton.isChecked():
                self.par_line_spinBox_5.setValue(self.data_from_field[0].x())
                self.par_line_spinBox_6.setValue(self.data_from_field[0].y())
                self.par_line_spinBox_9.setValue(self.data_from_field[1].x() - self.data_from_field[0].x())
                self.par_line_spinBox_10.setValue(self.data_from_field[1].y() - self.data_from_field[0].y())
                self.par_line_spinBox_7.setValue(self.data_from_field[2].x())
                self.par_line_spinBox_8.setValue(self.data_from_field[2].y())
                self.par_line_spinBox_11.setValue(self.data_from_field[3].x() - self.data_from_field[2].x())
                self.par_line_spinBox_12.setValue(self.data_from_field[3].y() - self.data_from_field[2].y())
            elif self.bez_radioButton.isChecked() or self.b_splain_radioButton.isChecked():
                self.par_line_spinBox_5.setValue(self.data_from_field[0].x())
                self.par_line_spinBox_6.setValue(self.data_from_field[0].y())
                self.par_line_spinBox_9.setValue(self.data_from_field[2].x())
                self.par_line_spinBox_10.setValue(self.data_from_field[2].y())
                self.par_line_spinBox_7.setValue(self.data_from_field[1].x())
                self.par_line_spinBox_8.setValue(self.data_from_field[1].y())
                self.par_line_spinBox_11.setValue(self.data_from_field[3].x())
                self.par_line_spinBox_12.setValue(self.data_from_field[3].y())
        self.data_from_field.clear()
        self.update()

    def lbl_move_event_handler(self, e):
        if e.pos().x() > 0 and e.pos().y() > 0 and self.mouse_cur_pos.x() > 0 and self.mouse_cur_pos.y() > 0 and self.lbl_pressed:
            pos = e.pos() - self.mouse_cur_pos
            self.pm_cur_pos += pos
            #print(e.pos()-self.mouse_cur_pos)
            #self.field_label.setPixmap(self.pm)
            self.update()
        self.coords_label.setText(f"x: {e.pos().x() // self.pix_rat - self.pm_cur_pos.x()} | y: {H - (e.pos().y() // self.pix_rat - self.pm_cur_pos.y()) - 1}")
        self.mouse_cur_pos = e.pos()
            # self.field_label.move(e.pos()-e.oldPos())

    def clear_pm(self):
        self.pm.fill(QColor(255, 255, 255, 255))
        self.field_label.setPixmap(self.pm)
        self.model.clear()
        self.update()

    def mouse_move_handler(self, e):
        print(1)
        if e.type() == QEvent.Type.MouseMove:
            print(1)
        return super().event(e)

    def field_paint_handler(self, e):
        self.field_label.setPixmap(self.real_pm)


app = QApplication(sys.argv)
mw = MainWindow()
app.exec()
