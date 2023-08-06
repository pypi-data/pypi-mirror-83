# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from server import Server
from threading import Thread


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(331, 482)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(331, 482))
        MainWindow.setMinimumSize(QtCore.QSize(331, 482))
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet("background-color: #28AFB0;")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(
            self.centralwidget)
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(30, 100, 81, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.addrLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.addrLabel.setFont(font)
        self.addrLabel.setStyleSheet("color: #ffffff;")
        self.addrLabel.setAlignment(QtCore.Qt.AlignRight |
                                    QtCore.Qt.AlignTrailing |
                                    QtCore.Qt.AlignVCenter)
        self.addrLabel.setObjectName("addrLabel")
        self.verticalLayout.addWidget(self.addrLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.portLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.portLabel.setFont(font)
        self.portLabel.setStyleSheet("color: #ffffff;")
        self.portLabel.setAlignment(QtCore.Qt.AlignRight |
                                    QtCore.Qt.AlignTrailing |
                                    QtCore.Qt.AlignVCenter)
        self.portLabel.setObjectName("portLabel")
        self.verticalLayout.addWidget(self.portLabel)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.dbLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dbLabel.setFont(font)
        self.dbLabel.setStyleSheet("color: #ffffff;")
        self.dbLabel.setAlignment(QtCore.Qt.AlignRight |
                                  QtCore.Qt.AlignTrailing |
                                  QtCore.Qt.AlignVCenter)
        self.dbLabel.setObjectName("dbLabel")
        self.verticalLayout.addWidget(self.dbLabel)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(
            QtCore.QRect(120, 100, 174, 131))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.ipText = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.ipText.setStyleSheet("background-color: rgb(155, 232, 232);")
        self.ipText.setObjectName("ipText")
        self.verticalLayout_2.addWidget(self.ipText)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.portText = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.portText.setStyleSheet("background-color: rgb(155, 232, 232);")
        self.portText.setObjectName("portText")
        self.verticalLayout_2.addWidget(self.portText)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.dbText = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.dbText.setStyleSheet("background-color: rgb(155, 232, 232);")
        self.dbText.setObjectName("dbText")
        self.verticalLayout_2.addWidget(self.dbText)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.maxconnLabel = QtWidgets.QLabel(self.centralwidget)
        self.maxconnLabel.setGeometry(QtCore.QRect(140, 236, 111, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.maxconnLabel.setFont(font)
        self.maxconnLabel.setStyleSheet("color: #ffffff;")
        self.maxconnLabel.setObjectName("maxconnLabel")
        self.maxconnVal = QtWidgets.QSpinBox(self.centralwidget)
        self.maxconnVal.setGeometry(QtCore.QRect(253, 236, 41, 18))
        self.maxconnVal.setStyleSheet("background-color: rgb(155, 232, 232);")
        self.maxconnVal.setFrame(True)
        self.maxconnVal.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.maxconnVal.setProperty("value", 5)
        self.maxconnVal.setObjectName("maxconnVal")
        self.onoffColor = QtWidgets.QLabel(self.centralwidget)
        self.onoffColor.setGeometry(QtCore.QRect(138, 300, 21, 21))
        self.onoffColor.setStyleSheet("border-style: outset;\n"
                                      "border-width: 2px;\n"
                                      "border-color: #ffffff;\n"
                                      "border-radius: 10px;\n"
                                      "background-color: rgb(211, 0, 0);")
        self.onoffColor.setFrameShape(QtWidgets.QFrame.Box)
        self.onoffColor.setFrameShadow(QtWidgets.QFrame.Plain)
        self.onoffColor.setObjectName("onoffColor")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(
            QtCore.QRect(32, 294, 271, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.liveLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.liveLabel.setFont(font)
        self.liveLabel.setStyleSheet("color: #ffffff;")
        self.liveLabel.setObjectName("liveLabel")
        self.horizontalLayout.addWidget(self.liveLabel)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20,
                                            QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20,
                                             QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.usersonlLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.usersonlLabel.setFont(font)
        self.usersonlLabel.setStyleSheet("color: #ffffff;")
        self.usersonlLabel.setObjectName("usersonlLabel")
        self.horizontalLayout.addWidget(self.usersonlLabel)
        self.usersonlVal = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.usersonlVal.sizePolicy().hasHeightForWidth())
        self.usersonlVal.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.usersonlVal.setFont(font)
        self.usersonlVal.setStyleSheet("color: #ffffff;")
        self.usersonlVal.setAlignment(QtCore.Qt.AlignCenter)
        self.usersonlVal.setObjectName("usersonlVal")
        self.horizontalLayout.addWidget(self.usersonlVal)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20,
                                             QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(22, 274, 291, 61))
        self.label_10.setStyleSheet("color: #ffffff;\n"
                                    "border-style: outset;\n"
                                    "border-width: 1px;\n"
                                    "border-color: #ffffff;\n"
                                    "border-radius: 8px;")
        self.label_10.setAlignment(QtCore.Qt.AlignHCenter |
                                   QtCore.Qt.AlignTop)
        self.label_10.setObjectName("label_10")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(60, 360, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.startButton.setFont(font)
        self.startButton.setStyleSheet("background-color: #A8F0AE ;\n"
                                       "border-style: solid;\n"
                                       "border-width: 1px;\n"
                                       "border-color: #ffffff;\n"
                                       "border-radius: 10px;")
        self.startButton.setObjectName("startButton")
        self.offButton = QtWidgets.QPushButton(self.centralwidget)
        self.offButton.setGeometry(QtCore.QRect(60, 410, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.offButton.setFont(font)
        self.offButton.setStyleSheet("background-color: #FF9D85 ;\n"
                                     "border-style: outset;\n"
                                     "border-width: 1px;\n"
                                     "border-color: #ffffff;\n"
                                     "border-radius: 10px;")
        self.offButton.setObjectName("offButton")
        self.offButton.setDisabled(True)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(20, 80, 291, 181))
        self.label_11.setStyleSheet("color: #ffffff;\n"
                                    "border-style: outset;\n"
                                    "border-width: 1px;\n"
                                    "border-color: #ffffff;\n"
                                    "border-radius: 8px;")
        self.label_11.setAlignment(QtCore.Qt.AlignHCenter |
                                   QtCore.Qt.AlignTop)
        self.label_11.setObjectName("label_11")
        self.label_11.raise_()
        self.label_10.raise_()
        self.label.raise_()
        self.verticalLayoutWidget.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.maxconnLabel.raise_()
        self.maxconnVal.raise_()
        self.horizontalLayoutWidget.raise_()
        self.onoffColor.raise_()
        self.startButton.raise_()
        self.offButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.startButton.clicked.connect(self.start_server)
        self.offButton.clicked.connect(self.stop_server)

        self.server = Server()
        self.serv_loop = Thread()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start()

    def updateStatus(self):

        if self.serv_loop.is_alive():

            self.usersonlVal.setText(str(len(self.server.all_clients)))

            self.onoffColor.setStyleSheet("border-style: outset;\n"
                                          "border-width: 2px;\n"
                                          "border-color: #ffffff;\n"
                                          "border-radius: 10px;\n"
                                          "background-color: #47FF33;")
        else:
            self.usersonlVal.setText("0")

            self.onoffColor.setStyleSheet("border-style: outset;\n"
                                          "border-width: 2px;\n"
                                          "border-color: #ffffff;\n"
                                          "border-radius: 10px;\n"
                                          "background-color: rgb(211, 0, 0);")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Server Manager"))
        self.addrLabel.setText(_translate("MainWindow", "Host Address:"))
        self.portLabel.setText(_translate("MainWindow", "Host Port:"))
        self.dbLabel.setText(_translate("MainWindow", "Server DB:"))
        self.ipText.setPlaceholderText(
            _translate("MainWindow", "Enter server ip..."))
        self.portText.setPlaceholderText(
            _translate("MainWindow", "Enter port number..."))
        self.dbText.setPlaceholderText(
            _translate("MainWindow", "Leave empty for default DB..."))
        self.maxconnLabel.setText(
            _translate("MainWindow", "Max. Connections:"))
        self.onoffColor.setText(_translate("MainWindow", " "))
        self.liveLabel.setText(_translate("MainWindow", "Server Live:"))
        self.usersonlLabel.setText(_translate("MainWindow", "Users Online:"))
        self.usersonlVal.setText(_translate("MainWindow", "0"))
        self.label_10.setText(_translate("MainWindow", "Server Status"))
        self.startButton.setText(_translate("MainWindow", "Launch"))
        self.offButton.setText(_translate("MainWindow", "Shut Down"))
        self.label_11.setText(_translate("MainWindow", "Server Settings"))

    def start_server(self):

        if self.server is None:
            ip = None
            if self.ipText.text():
                try:
                    ip = self.ipText.text()
                except Exception:
                    pass

            port = None
            if self.portText.text():
                try:
                    port = int(self.portText.text())
                except Exception:
                    pass

            self.server = self.server.port = port, self.server.addr = ip
        self.server.run = True
        self.serv_loop = Thread(target=self.server.mainloop, args=())
        self.serv_loop.start()
        self.arrange_while_running()

    def arrange_while_running(self):
        self.startButton.setDisabled(True)
        self.ipText.setDisabled(True)
        self.portText.setDisabled(True)
        self.dbText.setDisabled(True)
        self.maxconnVal.setDisabled(True)

        self.offButton.setDisabled(False)

    def arrange_while_idle(self):
        self.offButton.setDisabled(True)

        self.ipText.setDisabled(False)
        self.portText.setDisabled(False)
        self.startButton.setDisabled(False)
        self.dbText.setDisabled(False)
        self.maxconnVal.setDisabled(False)

    def stop_server(self):
        self.server.run = False

        self.arrange_while_idle()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
