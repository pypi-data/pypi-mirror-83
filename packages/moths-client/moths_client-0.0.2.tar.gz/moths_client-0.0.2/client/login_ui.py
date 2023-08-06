# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from client import Client
from _thread import start_new_thread
import hashlib


class Login_Ui(object):

    def setupUi(self, MainWindow, main_trigger, main_ui, reg_ui):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(410, 269)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #28AFB0;\n")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 10, 376, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.addressText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.addressText.setStyleSheet("background-color: #9BE8E8;")
        self.addressText.setText("")
        self.addressText.setObjectName("addressText")
        self.gridLayout.addWidget(self.addressText, 4, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 5, 1, 1)
        self.usernameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setStyleSheet("background-color: #28AFB0;\n"
                                         "color: #ffffff;\n")
        self.usernameLabel.setObjectName("usernameLabel")
        self.gridLayout.addWidget(self.usernameLabel, 5, 2, 1, 1)
        self.portText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.portText.sizePolicy().hasHeightForWidth())
        self.portText.setSizePolicy(sizePolicy)
        self.portText.setMaximumSize(QtCore.QSize(60, 16777215))
        self.portText.setStyleSheet("background-color: #9BE8E8;")
        self.portText.setObjectName("portText")
        self.gridLayout.addWidget(self.portText, 4, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.serverLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.serverLabel.setFont(font)
        self.serverLabel.setStyleSheet("background-color: #28AFB0;\n"
                                       "color: #ffffff;")
        self.serverLabel.setObjectName("serverLabel")
        self.gridLayout.addWidget(self.serverLabel, 4, 2, 1, 1)
        self.chatName = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        # font.setPointSize(18)
        self.chatName.setFont(font)
        self.chatName.setStyleSheet("background-color: #28AFB0;\n"
                                    "font: 87 12pt \"Arial Black\";"
                                    "color: #ffffff;")
        self.chatName.setAlignment(QtCore.Qt.AlignCenter)
        self.chatName.setObjectName("chatName")

        self.logo_lbl = QtWidgets.QLabel(self.centralwidget)
        self.logo_pixmap = QtGui.QPixmap("common/moths_logo.png")
        self.logo_lbl.setPixmap(self.logo_pixmap)
        self.logo_lbl.setGeometry(102, 43, 91, 50)

        self.gridLayout.addWidget(self.chatName, 1, 1, 1, 4)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 6, 1, 1, 1)
        self.usernameText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.usernameText.sizePolicy().hasHeightForWidth())
        self.usernameText.setSizePolicy(sizePolicy)
        self.usernameText.setStyleSheet("background-color: #9BE8E8;")
        self.usernameText.setObjectName("usernameText")
        self.gridLayout.addWidget(self.usernameText, 5, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)

        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(58, 220, 132, 23))
        self.loginButton.setStyleSheet("background-color: #CDF4F4;\n"
                                       "color: #1D8686;\n"
                                       "font: 75 9pt \"Arial\";")

        self.registerButton = QtWidgets.QPushButton(self.centralwidget)
        self.registerButton.setGeometry(QtCore.QRect(218, 220, 132, 23))
        self.registerButton.setStyleSheet("background-color: #CDF4F4;\n"
                                          "color: #1D8686;\n"
                                          "font: 75 9pt \"Arial\";")

        self.passLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passLabel.setFont(font)
        self.passLabel.setStyleSheet("background-color: #28AFB0;\n"
                                     "color: #ffffff;\n")
        self.passLabel.setObjectName("passLabel")
        self.gridLayout.addWidget(self.passLabel, 6, 2, 1, 1)
        self.passText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.passText.sizePolicy().hasHeightForWidth())
        self.passText.setSizePolicy(sizePolicy)
        self.passText.setStyleSheet("background-color: #9BE8E8;")
        self.passText.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.passText.setObjectName("passText")
        self.passText.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gridLayout.addWidget(self.passText, 6, 3, 1, 1)

        self.warningLabel = QtWidgets.QLabel(self.centralwidget)
        self.warningLabel.setGeometry(QtCore.QRect(90, 187, 251, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.warningLabel.setFont(font)
        self.warningLabel.setStyleSheet("color: rgb(250, 0, 0);")
        self.warningLabel.setAlignment(
            QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.warningLabel.setObjectName("warningLabel")

        self.main_trigger = main_trigger
        self.main_ui = main_ui

        self.reg_ui = reg_ui

        self.loginButton.setObjectName("loginButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.loginButton.clicked.connect(self.launch_main)
        self.registerButton.clicked.connect(self.launch_register)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.warning_timer = QtCore.QTimer()
        self.warning_timer.setInterval(3000)
        self.warning_timer.setSingleShot(True)
        self.warning_timer.timeout.connect(self.wipe_warning)

        self.auth_timer = QtCore.QTimer()
        self.auth_timer.setInterval(1000)
        self.auth_timer.setSingleShot(True)
        self.auth_timer.timeout.connect(self.check_auth)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addressText.setPlaceholderText(
            _translate("MainWindow", "Address"))
        self.usernameLabel.setText(_translate("MainWindow", "Username"))
        self.portText.setPlaceholderText(_translate("MainWindow", "Port"))
        self.serverLabel.setText(_translate("MainWindow", "Server"))
        self.chatName.setText(_translate("MainWindow", "                 Client Auth."))
        self.passLabel.setText(_translate("MainWindow", "Password"))
        self.loginButton.setText(_translate("MainWindow", "Connect"))
        self.registerButton.setText(_translate("MainWindow", "Register"))

    def fetch_details(self):
        hash = hashlib.md5(self.passText.text().encode())
        hash = hash.digest()

        return [self.addressText.text(),
                self.portText.text(), self.usernameText.text(), hash]

    def launch_main(self):

        if not self.auth_timer.isActive():
            login_details = self.fetch_details()
            # login_app.exit()

            self.main_ui.client = Client(server=login_details[0],
                                         port=login_details[1],
                                         username=login_details[2],
                                         password=login_details[3],
                                         gui_out=self.main_ui)
            self.main_ui.client.auth_action = "login"
            start_new_thread(self.main_ui.client.mainloop, ())
            self.auth_timer.start()

    def launch_register(self):

        self.main_ui.login_window.hide()
        self.main_ui.reg_window.show()

    def register_client(self):

        self.main_ui.reg_window.hide()

        if not self.auth_timer.isActive():

            reg_details = self.reg_ui.fetch_details()

            self.main_ui.client = Client(server=reg_details[0],
                                         port=reg_details[1],
                                         username=reg_details[2],
                                         password=reg_details[3],
                                         fullname=reg_details[4],
                                         email=reg_details[5],
                                         gui_out=self.main_ui)
            self.main_ui.client.auth_action = "register"
            start_new_thread(self.main_ui.client.mainloop, ())
            self.auth_timer.start()

    def check_auth(self):
        if not self.main_ui.authenticated:
            self.warning_message("Wrong credentials! (login/password)")
        else:
            self.main_trigger()

    def wipe_warning(self):
        if self.warningLabel.text():
            self.warningLabel.setText("")

    def warning_message(self, warning):
        self.warningLabel.setText(warning)
        self.warning_timer.start()
