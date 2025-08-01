# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debug.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1413, 1033)
        self.layoutWidget_3 = QtWidgets.QWidget(Form)
        self.layoutWidget_3.setGeometry(QtCore.QRect(27, 777, 1331, 161))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.textEdit_input = QtWidgets.QTextEdit(self.layoutWidget_3)
        self.textEdit_input.setMinimumSize(QtCore.QSize(1000, 0))
        self.textEdit_input.setObjectName("textEdit_input")
        self.horizontalLayout_9.addWidget(self.textEdit_input)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_send = QtWidgets.QPushButton(self.layoutWidget_3)
        self.pushButton_send.setMinimumSize(QtCore.QSize(150, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton_send.setFont(font)
        self.pushButton_send.setObjectName("pushButton_send")
        self.verticalLayout.addWidget(self.pushButton_send)
        self.pushButton_cleansend = QtWidgets.QPushButton(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton_cleansend.setFont(font)
        self.pushButton_cleansend.setObjectName("pushButton_cleansend")
        self.verticalLayout.addWidget(self.pushButton_cleansend)
        self.horizontalLayout_9.addLayout(self.verticalLayout)
        self.layoutWidget_4 = QtWidgets.QWidget(Form)
        self.layoutWidget_4.setGeometry(QtCore.QRect(30, 70, 1331, 681))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.textEdit_display = QtWidgets.QTextEdit(self.layoutWidget_4)
        self.textEdit_display.setEnabled(True)
        self.textEdit_display.setObjectName("textEdit_display")
        self.horizontalLayout_10.addWidget(self.textEdit_display)
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget_4)
        self.groupBox.setMinimumSize(QtCore.QSize(350, 0))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox_data = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_data.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_data.setObjectName("comboBox_data")
        self.horizontalLayout_3.addWidget(self.comboBox_data)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.checkBox_save = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_save.setObjectName("checkBox_save")
        self.horizontalLayout_8.addWidget(self.checkBox_save)
        self.gridLayout.addLayout(self.horizontalLayout_8, 8, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_baud = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_baud.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_baud.setObjectName("comboBox_baud")
        self.horizontalLayout.addWidget(self.comboBox_baud)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox_stop = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_stop.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_stop.setObjectName("comboBox_stop")
        self.horizontalLayout_2.addWidget(self.comboBox_stop)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox_16dispaly = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_16dispaly.setChecked(True)
        self.checkBox_16dispaly.setObjectName("checkBox_16dispaly")
        self.horizontalLayout_11.addWidget(self.checkBox_16dispaly)
        self.checkBox_time = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_time.setChecked(True)
        self.checkBox_time.setObjectName("checkBox_time")
        self.horizontalLayout_11.addWidget(self.checkBox_time)
        self.gridLayout.addLayout(self.horizontalLayout_11, 7, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_save = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_6.addWidget(self.pushButton_save)
        self.pushButton_clean = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_clean.setObjectName("pushButton_clean")
        self.horizontalLayout_6.addWidget(self.pushButton_clean)
        self.gridLayout.addLayout(self.horizontalLayout_6, 6, 0, 1, 1)
        self.comboBox_com = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_com.setMaximumSize(QtCore.QSize(326, 16777215))
        self.comboBox_com.setObjectName("comboBox_com")
        self.gridLayout.addWidget(self.comboBox_com, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.comboBox_check = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_check.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_check.setObjectName("comboBox_check")
        self.horizontalLayout_4.addWidget(self.comboBox_check)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_openclose = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_openclose.setObjectName("pushButton_openclose")
        self.horizontalLayout_5.addWidget(self.pushButton_openclose)
        self.gridLayout.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.horizontalLayout_10.addWidget(self.groupBox)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 10, 1331, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_33 = QtWidgets.QLabel(self.widget)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_7.addWidget(self.label_33)
        self.pushButton_control_model = QtWidgets.QPushButton(self.widget)
        self.pushButton_control_model.setObjectName("pushButton_control_model")
        self.horizontalLayout_7.addWidget(self.pushButton_control_model)
        self.pushButton_watchwindow = QtWidgets.QPushButton(self.widget)
        self.pushButton_watchwindow.setObjectName("pushButton_watchwindow")
        self.horizontalLayout_7.addWidget(self.pushButton_watchwindow)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setGeometry(QtCore.QRect(29, 950, 1331, 26))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.checkBox_16send = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_16send.setChecked(True)
        self.checkBox_16send.setObjectName("checkBox_16send")
        self.horizontalLayout_12.addWidget(self.checkBox_16send)
        self.checkBox_send_CRC_2 = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_send_CRC_2.setChecked(True)
        self.checkBox_send_CRC_2.setObjectName("checkBox_send_CRC_2")
        self.horizontalLayout_12.addWidget(self.checkBox_send_CRC_2)
        self.label_5 = QtWidgets.QLabel(self.widget1)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_12.addWidget(self.label_5)
        self.toolButton_help = QtWidgets.QToolButton(self.widget1)
        self.toolButton_help.setObjectName("toolButton_help")
        self.horizontalLayout_12.addWidget(self.toolButton_help)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_send.setText(_translate("Form", "发送"))
        self.pushButton_cleansend.setText(_translate("Form", "清除发送"))
        self.groupBox.setTitle(_translate("Form", "串口选择"))
        self.label_3.setText(_translate("Form", "数据位："))
        self.checkBox_save.setText(_translate("Form", "自动保存"))
        self.label.setText(_translate("Form", "波特率："))
        self.label_2.setText(_translate("Form", "停止位："))
        self.checkBox_16dispaly.setText(_translate("Form", "16进制显示"))
        self.checkBox_time.setText(_translate("Form", "时间戳"))
        self.pushButton_save.setText(_translate("Form", "保存窗口"))
        self.pushButton_clean.setText(_translate("Form", "清除接收"))
        self.label_4.setText(_translate("Form", "校验位："))
        self.pushButton_openclose.setText(_translate("Form", "打开串口"))
        self.label_33.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">调试模式</span></p></body></html>"))
        self.pushButton_control_model.setText(_translate("Form", "控制模式"))
        self.pushButton_watchwindow.setText(_translate("Form", "观测窗口"))
        self.checkBox_16send.setText(_translate("Form", "16进制发送"))
        self.checkBox_send_CRC_2.setText(_translate("Form", "CRC校验尾补充"))
        self.label_5.setText(_translate("Form", "Copyright © 2025 Bruce Lee (USTC). All Rights Reserved."))
        self.toolButton_help.setText(_translate("Form", "help"))
