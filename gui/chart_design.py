# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chart_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 512)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_market = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_market.setGeometry(QtCore.QRect(200, 10, 221, 22))
        self.comboBox_market.setObjectName("comboBox_market")
        self.comboBox_timeframe = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_timeframe.setGeometry(QtCore.QRect(450, 10, 81, 22))
        self.comboBox_timeframe.setObjectName("comboBox_timeframe")
        self.lineEdit_quick = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_quick.setGeometry(QtCore.QRect(800, 40, 41, 20))
        self.lineEdit_quick.setObjectName("lineEdit_quick")
        self.lineEdit_fast = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_fast.setGeometry(QtCore.QRect(800, 70, 41, 20))
        self.lineEdit_fast.setObjectName("lineEdit_fast")
        self.lineEdit_middle = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_middle.setGeometry(QtCore.QRect(800, 100, 41, 20))
        self.lineEdit_middle.setObjectName("lineEdit_middle")
        self.lineEdit_slow = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_slow.setGeometry(QtCore.QRect(800, 130, 41, 20))
        self.lineEdit_slow.setObjectName("lineEdit_slow")
        self.label_quick = QtWidgets.QLabel(self.centralwidget)
        self.label_quick.setGeometry(QtCore.QRect(760, 42, 50, 12))
        self.label_quick.setObjectName("label_quick")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(760, 70, 50, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(760, 100, 50, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(760, 130, 50, 12))
        self.label_4.setObjectName("label_4")
        self.pushButton_draw = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_draw.setGeometry(QtCore.QRect(780, 320, 75, 31))
        self.pushButton_draw.setObjectName("pushButton_draw")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 40, 741, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_debug1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_debug1.setGeometry(QtCore.QRect(780, 360, 75, 31))
        self.pushButton_debug1.setObjectName("pushButton_debug1")
        self.pushButton_debug2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_debug2.setGeometry(QtCore.QRect(780, 400, 75, 31))
        self.pushButton_debug2.setObjectName("pushButton_debug2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 880, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_quick.setText(_translate("MainWindow", "Quick"))
        self.label_2.setText(_translate("MainWindow", "Fast"))
        self.label_3.setText(_translate("MainWindow", "Middle"))
        self.label_4.setText(_translate("MainWindow", "Slow"))
        self.pushButton_draw.setText(_translate("MainWindow", "draw"))
        self.pushButton_debug1.setText(_translate("MainWindow", "debug1"))
        self.pushButton_debug2.setText(_translate("MainWindow", "debug2"))
