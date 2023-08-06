# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from login_ui import Login_Ui
from register_ui import Register_Ui


class clickable_Label(QtWidgets.QLabel):

    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):

        QtWidgets.QLabel.__init__(self, parent)

        self.chosen = False

    def check(self):
        if not self.chosen:
            self.chosen = True
            self.setStyleSheet("background-color: #DB2955")

    def uncheck(self):
        if self.chosen:
            self.chosen = False
            self.setStyleSheet("background-color: rgb(222, 243, 240);")

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.clicked.emit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 434)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(640, 434))
        MainWindow.setMinimumSize(QtCore.QSize(640, 434))

        self.threadpool = QtCore.QThreadPool()

        self.login_window = None
        self.reg_window = None
        self.main_window = None

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: #28AFB0;\n"
                                         "")
        self.centralwidget.setObjectName("centralwidget")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(430, 370, 191, 41))
        self.sendButton.setStyleSheet("background-color: #CDF4F4;\n"
                                      "color: #1D8686;\n"
                                      "font: 75 12pt \"Arial\";")
        self.sendButton.setObjectName("sendButton")
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(220, 370, 191, 41))
        self.clearButton.setStyleSheet("background-color: #CDF4F4;\n"
                                       "color: #1D8686;\n"
                                       "font: 75 12pt \"Arial\";")
        self.clearButton.setObjectName("clearButton")

        self.chatScroll = QtWidgets.QScrollArea(self.centralwidget)
        self.chatScroll.setGeometry(QtCore.QRect(220, 60, 401, 211))
        self.chatScroll.setStyleSheet("background-color: #CDF4F4;\n"
                                      "color: #1D8686;\n"
                                      "font: 75 9pt \"Arial\";")
        self.chatWidget = QtWidgets.QWidget()
        self.chatvbox = QtWidgets.QVBoxLayout()
        self.chatScroll.setWidgetResizable(True)

        self.chatWidget.setLayout(self.chatvbox)

        self.chatScroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.chatScroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.chatScroll.setWidget(self.chatWidget)

        self.logo_lbl = QtWidgets.QLabel(self.centralwidget)
        self.logo_pixmap = QtGui.QPixmap("common/moths_logo.png")
        self.logo_lbl.setPixmap(self.logo_pixmap)
        self.logo_lbl.setGeometry(526, 6, 91, 50)

        self.contactsScreen = QtWidgets.QGroupBox(self.centralwidget)
        self.contactsScreen.setGeometry(QtCore.QRect(20, 60, 181, 291))
        self.contactsScreen.setStyleSheet("background-color: #9BE8E8;")
        self.contactsScreen.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.contactsScreen.setFlat(True)
        self.contactsScreen.setObjectName("contactsScreen")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.contactsScreen)
        self.verticalLayout.setContentsMargins(0, 1, 0, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contactsList = QtWidgets.QVBoxLayout()
        self.contactsList.setObjectName("contactsList")
        self.addContactText = QtWidgets.QLineEdit(self.contactsScreen)
        self.addContactText.setStyleSheet("background-color: #ffffff")
        self.addContactText.setObjectName("ContactTextLine")
        self.verticalLayout.addWidget(self.addContactText)
        self.addContact = QtWidgets.QPushButton(self.contactsScreen)
        self.addContact.setStyleSheet("background-color: rgb(222, 243, 240);")
        self.addContact.setDefault(False)
        self.addContact.setFlat(False)
        self.addContact.setObjectName("addContact")
        self.contactsList.addWidget(self.addContact)
        self.verticalLayout.addLayout(self.contactsList)
        self.spacerItem = QtWidgets.QSpacerItem(
            20, 40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.spacerItem)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(220, 280, 401, 71))
        self.textEdit.setStyleSheet("background-color: #CDF4F4;\n"
                                    "color: #1D8686;\n"
                                    "font: 75 9pt \"Arial\";")
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.sendButton.clicked.connect(self.sendMessage)
        self.clearButton.clicked.connect(self.clearInput)
        self.addContact.clicked.connect(
            lambda: self.add_contact(self.addContactText.text()))

        self.authenticated = False

        self.temp = []

        self.client = None

        self.contact_buttons = []
        self.contacts_list = []

        self.chosen_contact = "all"

        self.chat_is_Empty = True

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.refreshScreen)
        self.timer.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.addContact.setText(_translate("MainWindow", "add contact..."))
        self.addContactText.setPlaceholderText(
            _translate("MainWindow", "Enter a username..."))

    def window_switch(self):
        self.login_window.hide()
        self.main_window.show()

    def add_contact(self, contact):
        self.addContactText.clear()

        self.contact_buttons.append(clickable_Label(self.contactsScreen))
        self.contactsList.addWidget(self.contact_buttons[-1])
        self.contact_buttons[-1].setText(contact)
        self.contact_buttons[-1].setObjectName(contact)
        self.contact_buttons[-1].setStyleSheet(
            "background-color: rgb(222, 243, 240);")
        self.contact_buttons[-1].setContentsMargins(5, 5, 5, 5)
        self.contact_buttons[-1].clicked.connect(
            lambda: self.choose_contact(contact))

    def clear_chat(self):
        for i in reversed(range(self.chatvbox.count())):
            try:
                self.chatvbox.itemAt(i).widget().setParent(None)
            except Exception:
                pass

    def choose_contact(self, target):

        self.chosen_contact = target

        self.clear_chat()

        self.chat_is_Empty = True

        for cont in self.contact_buttons:
            if cont.text() != target:
                cont.uncheck()
            else:
                cont.check()

    def refreshScreen(self):
        try:
            if self.client.isConnected:
                cont_list = self.client.contacts()
                for user in cont_list:
                    if user not in self.contacts_list:
                        self.contacts_list.append(user)
                        self.add_contact(user)

                chat_messages = self.client.load_chat(self.chosen_contact)

                if self.client.pending_message or self.chat_is_Empty:
                    self.clear_chat()

                    for message in chat_messages:
                        temp_line = QtWidgets.QLabel(self.chatWidget)
                        temp_line.setContentsMargins(10, 10, 10, 10)
                        temp_line.setText(
                            message["sender"]+":\n\n"+message["message"])

                        temp_line.setSizePolicy(
                            QtWidgets.QSizePolicy(
                                QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Fixed))

                        if self.client.account_name == message["sender"]:
                            temp_line.setStyleSheet(
                                "background-color: #70BFFF")
                            temp_line.setAlignment(QtCore.Qt.AlignRight)

                        else:
                            temp_line.setStyleSheet(
                                "background-color: #87C38F")
                            temp_line.setAlignment(QtCore.Qt.AlignLeft)

                        self.chatvbox.removeItem(self.spacerItem)
                        self.chatvbox.addWidget(temp_line)
                        self.chatvbox.addItem(self.spacerItem)

                    self.client.pending_message = False

                self.chat_is_Empty = False

        except Exception:
            pass

    def sendMessage(self):
        self.client.message(user=self.chosen_contact,
                            text=self.textEdit.toPlainText())

        self.textEdit.clear()

    def clearInput(self):
        self.textEdit.clear()


mainapp = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

login_app = QtWidgets.QApplication(sys.argv)
LoginWindow = QtWidgets.QMainWindow()
login_ui = Login_Ui()

registerapp = QtWidgets.QApplication(sys.argv)
RegisterWindow = QtWidgets.QMainWindow()
register_ui = Register_Ui()
register_ui.setupUi(RegisterWindow, main_ui=ui, login_ui=login_ui)

ui.login_window = LoginWindow
ui.main_window = MainWindow
ui.reg_window = RegisterWindow

login_ui.setupUi(LoginWindow, main_trigger=ui.window_switch,
                 main_ui=ui, reg_ui=register_ui)

LoginWindow.show()
sys.exit(login_app.exec_())
