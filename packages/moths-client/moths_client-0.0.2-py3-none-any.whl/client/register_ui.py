# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib


class Register_Ui(object):

    def setupUi(self, MainWindow, main_ui, login_ui):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(410, 363)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #28AFB0;\n")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 376, 255))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.passText_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.passText_2.sizePolicy().hasHeightForWidth())
        self.passText_2.setSizePolicy(sizePolicy)
        self.passText_2.setStyleSheet("background-color: #9BE8E8;")
        self.passText_2.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.passText_2.setObjectName("passText_2")
        self.gridLayout.addWidget(self.passText_2, 8, 3, 1, 1)
        self.passLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passLabel.setFont(font)
        self.passLabel.setStyleSheet("background-color: #28AFB0;\n"
                                     "color: #ffffff;\n")
        self.passLabel.setObjectName("passLabel")
        self.gridLayout.addWidget(self.passLabel, 7, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.usernameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setStyleSheet("background-color: #28AFB0;\n"
                                         "color: #ffffff;\n")
        self.usernameLabel.setObjectName("usernameLabel")
        self.gridLayout.addWidget(self.usernameLabel, 5, 2, 1, 1)
        self.chatName = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(27)
        self.chatName.setFont(font)
        self.chatName.setStyleSheet("background-color: #28AFB0;\n"
                                    "color: #ffffff;")
        self.chatName.setAlignment(QtCore.Qt.AlignCenter)
        self.chatName.setObjectName("chatName")
        self.gridLayout.addWidget(self.chatName, 1, 1, 1, 4)
        self.emailLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.emailLabel.setFont(font)
        self.emailLabel.setStyleSheet("background-color: #28AFB0;\n"
                                      "color: #ffffff;\n")
        self.emailLabel.setObjectName("emailLabel")
        self.gridLayout.addWidget(self.emailLabel, 9, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 5, 1, 1)
        self.passLabel_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passLabel_2.setFont(font)
        self.passLabel_2.setStyleSheet("background-color: #28AFB0;\n"
                                       "color: #ffffff;\n")
        self.passLabel_2.setObjectName("passLabel_2")
        self.gridLayout.addWidget(self.passLabel_2, 8, 2, 1, 1)
        self.emailText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.emailText.sizePolicy().hasHeightForWidth())
        self.emailText.setSizePolicy(sizePolicy)
        self.emailText.setStyleSheet("background-color: #9BE8E8;")
        self.emailText.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.emailText.setObjectName("emailText")
        self.gridLayout.addWidget(self.emailText, 9, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.usernameText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.usernameText.sizePolicy().hasHeightForWidth())
        self.usernameText.setSizePolicy(sizePolicy)
        self.usernameText.setStyleSheet("background-color: #9BE8E8;")
        self.usernameText.setObjectName("usernameText")
        self.gridLayout.addWidget(self.usernameText, 5, 3, 1, 1)
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
        self.gridLayout.addWidget(self.passText, 7, 3, 1, 1)
        self.fullnameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fullnameLabel.setFont(font)
        self.fullnameLabel.setStyleSheet("background-color: #28AFB0;\n"
                                         "color: #ffffff;\n")
        self.fullnameLabel.setObjectName("fullnameLabel")
        self.gridLayout.addWidget(self.fullnameLabel, 6, 2, 1, 1)
        self.fullnameText = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.fullnameText.sizePolicy().hasHeightForWidth())
        self.fullnameText.setSizePolicy(sizePolicy)
        self.fullnameText.setStyleSheet("background-color: #9BE8E8;")
        self.fullnameText.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.fullnameText.setObjectName("fullnameText")
        self.gridLayout.addWidget(self.fullnameText, 6, 3, 1, 1)
        self.passLabel_0 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passLabel_0.setFont(font)
        self.passLabel_0.setStyleSheet("background-color: #28AFB0;\n"
                                       "color: #ffffff;\n")
        self.passLabel_0.setAlignment(
            QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.passLabel_0.setObjectName("passLabel_4")
        self.gridLayout.addWidget(self.passLabel_0, 4, 2, 1, 1)
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(210, 320, 121, 23))
        self.loginButton.setStyleSheet("background-color: #CDF4F4;\n"
                                       "color: #1D8686;\n"
                                       "font: 75 9pt \"Arial\";")
        self.loginButton.setObjectName("loginButton")
        self.warningLabel = QtWidgets.QLabel(self.centralwidget)
        self.warningLabel.setGeometry(QtCore.QRect(100, 290, 211, 24))
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
        self.registerButton = QtWidgets.QPushButton(self.centralwidget)
        self.registerButton.setGeometry(QtCore.QRect(80, 320, 121, 23))
        self.registerButton.setStyleSheet("background-color: #CDF4F4;\n"
                                          "color: #1D8686;\n"
                                          "font: 75 9pt \"Arial\";")
        self.registerButton.setObjectName("registerButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.main_ui = main_ui
        self.login_ui = login_ui

        self.loginButton.clicked.connect(self.back_to_login)

        self.registerButton.clicked.connect(self.register)

        self.warning_timer = QtCore.QTimer()
        self.warning_timer.setInterval(3000)
        self.warning_timer.setSingleShot(True)
        self.warning_timer.timeout.connect(self.wipe_warning)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.passLabel.setText(_translate("MainWindow", "Password:"))
        self.usernameLabel.setText(_translate("MainWindow", "Username:"))
        self.chatName.setText(_translate("MainWindow", "Chat Auth."))
        self.emailLabel.setText(_translate("MainWindow", "Email:"))
        self.passLabel_2.setText(_translate("MainWindow", "Repeat Password:"))
        self.fullnameLabel.setText(_translate("MainWindow", "Full Name:"))
        self.passLabel_0.setText(
            _translate("MainWindow", "Registration Form:"))
        self.loginButton.setText(_translate("MainWindow", "Back"))
        self.warningLabel.setText(_translate("MainWindow", ""))
        self.registerButton.setText(_translate("MainWindow", "Register"))

    def back_to_login(self):
        self.main_ui.reg_window.hide()
        self.main_ui.login_window.show()

    def fetch_details(self):

        hash = hashlib.md5(self.passText.text().encode())
        hash = hash.digest()

        return [None, None, self.usernameText.text(),
                hash, self.fullnameText.text(), self.emailText.text()]

    def register(self):
        if self.passText.text() and self.passText_2.text() \
                and self.usernameText.text() and self.fullnameText.text() \
                and self.emailText.text():
            if self.passText.text() == self.passText_2.text():
                self.login_ui.register_client()
            else:
                self.warning_message("Password lines don't match!")
        else:
            self.warning_message("Please complete the form!")

    def wipe_warning(self):
        if self.warningLabel.text():
            self.warningLabel.setText("")

    def warning_message(self, warning):
        self.warningLabel.setText(warning)
        self.warning_timer.start()
