import os
import time
import requests
import threading
import re
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        font = QtGui.QFont()
        font.setFamily("HarmonyOS Sans SC Medium")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 80, 581, 321))
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 30, 581, 34))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.getid()
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.startButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(470, 420, 141, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.stopButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_2.addWidget(self.stopButton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "虎牙封面爬取"))
        self.label.setText(_translate("MainWindow", "               选择爬取的分区                   "))
        self.startButton.setText(_translate("MainWindow", "开始爬取"))
        self.startButton.clicked.connect(self.startdownload)
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.stopButton.clicked.connect(self.stopdownload)

    def getid(self):
        url = 'https://www.huya.com/g'

        res = requests.get(url).text

        responce = BeautifulSoup(res, "html.parser")

        lis = responce.find_all(name='li', class_="g-gameCard-item")

        for li in lis:
            reg1 = 'title="[^\x00-\xff]+"'
            reg2 = 'g/[a-zA-Z0-9]+'
            try:
                name = re.search(reg1, str(li)).group().split("=")[1].strip('"')
                id = re.search(reg2, str(li)).group().split("/")[1]
                self.comboBox.addItem(name + ":" + id)
            except BaseException:
                pass

    def startdownload(self):
        # 创建一个线程来执行get_pictures
        global t1
        t1 = threading.Thread(target=self.get_pictures)
        t1.start()

    def stopdownload(self):
        t1.stop()

    def get_pictures(self):
        i = 1
        global category
        category = self.comboBox.currentText().split(":")[0]
        id = self.comboBox.currentText().split(":")[1]
        url = "https://www.huya.com/g/" + id

        response = requests.get(url=url).content

        soup = BeautifulSoup(response, "html.parser")

        imgs = soup.find_all(name='img', class_="pic")

        if not os.path.exists("pictures/%s" % category):
            os.makedirs("pictures/%s" % category)

        self.textBrowser.append("开始下载 %s 分区直播封面" % category)
        for img in imgs:
            img_url = img['data-original']
            img_urlrec = img_url.split("?")[0]
            img_namerec = img['alt'].split('的')[0]

            # 在textBrower的文本框显示
            self.textBrowser.append("正在下载主播 " + img_namerec + "的封面")
            try:
                img_rec = requests.get(img_urlrec).content
                with open("pictures/%s/%s.%s.jpg" % (category, str(i), img_namerec), 'wb') as f:
                    f.write(img_rec)
                    # 线程休眠0.5秒
                    time.sleep(0.5)
                    i = i + 1
            except BaseException:
                self.textBrowser.append("主播：" + img_namerec + " 下载失败")
                pass

        self.textBrowser.append("%s分区直播封面下载完成" % category + "，共下载 %s 个封面" % str(i-1))
