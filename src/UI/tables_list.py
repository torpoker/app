# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tables_list.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(940, 656)
        MainWindow.setMinimumSize(QtCore.QSize(800, 656))
        MainWindow.setStyleSheet("#centralwidget{\n"
"background-color: rgb(85, 87, 83);\n"
"    border-image: url(./src/UI/images/TgFZH.jpg);\n"
"}\n"
"QStatusBar\n"
"{\n"
"    color: white;\n"
"    background-color: rgb(71, 71, 71);\n"
"    font: 9pt \"Montserrat\";\n"
"}\n"
"QStatusBar::item\n"
"{\n"
"    border: 0px transparent dark;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem2, 3, 1, 1, 1)
        self.tableWidget_game_tables = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_game_tables.setStyleSheet("QHeaderView{\n"
"    background-color: transparent; /* header background*/\n"
"}\n"
"QTableView{\n"
"    gridline-color: rgba(0,0,0,0);\n"
"}\n"
"QTableWidget{\n"
"    background-color: transparent; /*transparent to show bg image*/\n"
"    border: 0px solid transparent;\n"
"}\n"
"QTableView::item{\n"
"    color: white;\n"
"    background-image: url(./src/UI/images/asd1354.png); /*cell bg image*/\n"
"}\n"
"QTableWidget::item{\n"
"    padding-left: 15; /*cell spacing*/\n"
"    border: 2px solid transparent; /*transparent cell borders*/\n"
"}\n"
"QHeaderView::section {\n"
"    color: white;\n"
"    background-color: #343434;\n"
"    font-size: 14pt;\n"
"    padding: 2px;\n"
"    border: 1px solid #4a4a4a;\n"
"    margin: 2px;\n"
"}")
        self.tableWidget_game_tables.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_game_tables.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_game_tables.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_game_tables.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_game_tables.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_game_tables.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_game_tables.setShowGrid(False)
        self.tableWidget_game_tables.setRowCount(0)
        self.tableWidget_game_tables.setObjectName("tableWidget_game_tables")
        self.tableWidget_game_tables.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_game_tables.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_game_tables.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_game_tables.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_game_tables.setHorizontalHeaderItem(3, item)
        self.tableWidget_game_tables.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget_game_tables.horizontalHeader().setMinimumSectionSize(75)
        self.tableWidget_game_tables.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_game_tables.verticalHeader().setVisible(False)
        self.tableWidget_game_tables.verticalHeader().setDefaultSectionSize(40)
        self.tableWidget_game_tables.verticalHeader().setMinimumSectionSize(35)
        self.gridLayout.addWidget(self.tableWidget_game_tables, 2, 1, 1, 1)
        self.frame_header = QtWidgets.QFrame(self.centralwidget)
        self.frame_header.setMinimumSize(QtCore.QSize(25, 150))
        self.frame_header.setMaximumSize(QtCore.QSize(16777215, 180))
        self.frame_header.setStyleSheet("#frame_header{\n"
"    background-color: rgb(255, 255, 255);\n"
"    \n"
"}")
        self.frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header.setObjectName("frame_header")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_header)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.frame_header)
        self.label.setMinimumSize(QtCore.QSize(424, 50))
        self.label.setMaximumSize(QtCore.QSize(516, 94))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("./src/UI/images/YfZiodQJx.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.pushButton_playnow = QtWidgets.QPushButton(self.frame_header)
        self.pushButton_playnow.setStyleSheet("#pushButton_playnow{\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"#pushButton_playnow:pressed{\n"
"    background-color: rgba(203, 203, 203,200);\n"
"    margin-left: 10px;\n"
"    margin-top: 5px;\n"
"}")
        self.pushButton_playnow.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./src/UI/images/SIdWGYLm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_playnow.setIcon(icon)
        self.pushButton_playnow.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_playnow.setObjectName("pushButton_playnow")
        self.gridLayout_3.addWidget(self.pushButton_playnow, 0, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        self.frame_my_acc = QtWidgets.QFrame(self.frame_header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_my_acc.sizePolicy().hasHeightForWidth())
        self.frame_my_acc.setSizePolicy(sizePolicy)
        self.frame_my_acc.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_my_acc.setMaximumSize(QtCore.QSize(250, 16777215))
        self.frame_my_acc.setStyleSheet("#frame_my_acc{\n"
"border: 1px solid white;\n"
"border-left-color: black;\n"
"}")
        self.frame_my_acc.setObjectName("frame_my_acc")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_my_acc)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.frame_my_acc)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame.setStyleSheet("#frame{\n"
"border: 1px solid white;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMaximumSize(QtCore.QSize(25, 16777215))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("./src/UI/images/PKlFdpHZ.png"))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.frame_my_acc)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(165, 112))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 7)
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setMinimumSize(QtCore.QSize(27, 28))
        self.label_4.setMaximumSize(QtCore.QSize(27, 28))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("./src/UI/images/2aewqeE.png"))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_stack = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_stack.setFont(font)
        self.label_stack.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_stack.setObjectName("label_stack")
        self.horizontalLayout_2.addWidget(self.label_stack)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 2)
        self.pushButton_cashout = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_cashout.setStyleSheet("#pushButton_cashout{\n"
"    font: 75 10pt \"Noto Naskh Arabic UI\";\n"
"    color: white;\n"
"    background-color: maroon;\n"
"\n"
"}\n"
"#pushButton_cashout:pressed{\n"
"        background-color: rgba(85, 0, 0, 200);\n"
"    margin-left: 10px;\n"
"    margin-top: 5px;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./src/UI/images/UGAyPsHIM.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_cashout.setIcon(icon1)
        self.pushButton_cashout.setObjectName("pushButton_cashout")
        self.gridLayout_2.addWidget(self.pushButton_cashout, 2, 0, 1, 2)
        self.pushButton_refresh_account = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_refresh_account.setStyleSheet("#pushButton_refresh_account{\n"
"    color: white;\n"
"    background-color:white;\n"
"\n"
"}\n"
"#pushButton_refresh_account:pressed{\n"
"    background-color:white;\n"
"    margin-left: 3px;\n"
"    margin-top: 5px;\n"
"}")
        self.pushButton_refresh_account.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./src/UI/images/weq23AD.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_refresh_account.setIcon(icon2)
        self.pushButton_refresh_account.setObjectName("pushButton_refresh_account")
        self.gridLayout_2.addWidget(self.pushButton_refresh_account, 2, 2, 1, 1)
        self.label_user_icon = QtWidgets.QLabel(self.frame_2)
        self.label_user_icon.setText("")
        self.label_user_icon.setPixmap(QtGui.QPixmap("./src/UI/images/ksdfvQWC.png"))
        self.label_user_icon.setObjectName("label_user_icon")
        self.gridLayout_2.addWidget(self.label_user_icon, 0, 0, 2, 1)
        self.label_username = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        self.label_username.setFont(font)
        self.label_username.setAlignment(QtCore.Qt.AlignCenter)
        self.label_username.setWordWrap(True)
        self.label_username.setObjectName("label_username")
        self.gridLayout_2.addWidget(self.label_username, 0, 1, 1, 2)
        self.verticalLayout.addWidget(self.frame_2)
        self.gridLayout_3.addWidget(self.frame_my_acc, 0, 5, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 0, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 0, 7, 1, 1)
        self.gridLayout.addWidget(self.frame_header, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Torpoker"))
        item = self.tableWidget_game_tables.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_game_tables.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Blinds"))
        item = self.tableWidget_game_tables.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Seats"))
        self.label_2.setText(_translate("MainWindow", "MY ACCOUNT"))
        self.label_stack.setText(_translate("MainWindow", "120000"))
        self.pushButton_cashout.setStatusTip(_translate("MainWindow", "Logout"))
        self.pushButton_cashout.setText(_translate("MainWindow", "Cash Out"))
        self.pushButton_refresh_account.setStatusTip(_translate("MainWindow", "refresh account status"))
        self.label_username.setText(_translate("MainWindow", "anonymous"))
