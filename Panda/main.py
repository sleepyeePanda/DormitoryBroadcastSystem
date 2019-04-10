import os
import sys

os.system('pyuic5 base.ui -o ui.py')
os.system('pyrcc5 resources.qrc -o resources_rc.py')

from PyQt5 import QtWidgets, QtCore
from ui import *
import aiohttp
import asyncio
import multiprocessing
import datetime
#import beautifulsoup


class TimeChanger(QtCore.QThread):
    def __init__(self,ui):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda:print(datetime.datetime.now()))#self.changeTime)
        self.timer.start(1000)

    def changeTime(self):
        curDateTime = QtCore.QDateTime.currentDateTime()
        ui.dateLabel.setText(curDateTime.toString('%YYYY년 %MM월 %d일'))
        ui.timeLabel.setText(curDateTime.toString('%hh  %mm  %ss'))


class Manager:
    def __init__(self,ui):
        self.timeChanger = TimeChanger(ui)
        self.ui = ui
        self.ui.backButton.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.nextButton.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.backDust.clicked.connect(lambda:self.ui.stackedDust.setCurrentIndex(0))
        self.ui.nextDust.clicked.connect(lambda:self.ui.stackedDust.setCurrentIndex(1))
        self.ui.addButton.toggled.connect(lambda x:self.toggleForm(x))
        self.ui.showDialog.clicked.connect(self.showDialog)
        #self.ui.uploadButton.clicked.connect(self.uploadFile)
        #self.ui.nextButton.clicked.connect(self.getInfo)

    @QtCore.pyqtSlot(bool)
    def toggleForm(self, state):
        forms = [ui.label, ui.comboBox, ui.timeEdit, ui.lineEdit,ui.showDialog, ui.uploadButton]
        if state:
            for f in forms:
                f.show()
        else:
            for f in forms:
                f.hide()


    def showDialog(self):
        dialog = QtWidgets.QFileDialog()
        #dialog.setFilter()
        fileName = dialog.getOpenFileName()

        if fileName:
            self.ui.lineEdit.setText(fileName[0].split(r'/')[-1])

    # def uploadFile(self):
    #     day = ui.comboBox.currentText()
    #     ui.timeEdit.
    #     file = ui.lineEdit.text()

    def getInfo(self):
        global loop
        loop.run_until_complete(self.coro())


    async def fetch(self,session, url):
        async with session.get(url) as response:
            return await response.text()

    async def coro(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+'대전+유성구+날씨')
            print(html)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    manager = Manager(ui)
    MainWindow.show()
    loop = asyncio.get_event_loop()
    sys.exit(app.exec_())