# Form implementation generated from reading ui file 'imageFilter.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from PyQt6.QtGui import QPixmap
import numpy as np
import cv2
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path
import subprocess
import os


LIST_OF_ALL_FRAMES = []

desktopPath = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')


try:
    subprocess.call("mkdir " + str(desktopPath) + "/imagesToLabel", shell=True)
except exception as ex:
    print("an error occured creating new folder")

directoryToDumpFiles = str(desktopPath) + "/imagesToLabel"


def loadDatasetIntoMemory(pathToDataset):
    path = Path(pathToDataset).glob('*.jpg')
    #listOfFileNames = [str(fileName).replace(".jpg", "").replace(pathToImages, "").replace("/", "") for fileName in path if fileName.is_file()]
    listOfImages = [cv2.imread(str(fileName)) for fileName in path if fileName.is_file()]

    for frame in listOfImages:
        LIST_OF_ALL_FRAMES.append(frame)
    return



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(676, 729)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 641, 481))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 580, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 580, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 550, 491, 20))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(50, 620, 571, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 660, 151, 16))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(550, 650, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 550, 71, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 660, 191, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(550, 580, 113, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 676, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        self.label.setScaledContents(True)

        self.currentIndex = 0
        self.pathToDataset = ""
        self.pushButton.clicked.connect(self.pushButton1WasClicked)
        self.pushButton_2.clicked.connect(self.pushButton2WasClicked)
        self.pushButton_3.clicked.connect(self.pushButton3WasClicked)
        self.pushButton_4.clicked.connect(self.pushButton4WasClicked)


    def doSomethingWithSliderValue(self, value):
        self.currentIndex = value
        self.updateCurrentImage(LIST_OF_ALL_FRAMES[self.currentIndex])
        return



    def pushButton1WasClicked(self):
        if(self.pathToDataset):
            if(self.currentIndex - 1 >= 0):
                self.currentIndex -= 1
                self.updateCurrentImage(LIST_OF_ALL_FRAMES[self.currentIndex])
        return

    def pushButton2WasClicked(self):
        if(self.pathToDataset):
            if(self.currentIndex + 1 < len(LIST_OF_ALL_FRAMES)):
                self.currentIndex += 1
                self.updateCurrentImage(LIST_OF_ALL_FRAMES[self.currentIndex])
        return


    def pushButton3WasClicked(self):
        homeDir = str(Path.home())
        qfd = QFileDialog()
        self.pathToDataset = str(QFileDialog.getExistingDirectory(qfd ,"Select Directory", homeDir))
        if(self.pathToDataset):
            loadDatasetIntoMemory(self.pathToDataset)
            numberOfImagesWithLabels = len(LIST_OF_ALL_FRAMES)
            self.label_3.setText(str(numberOfImagesWithLabels) + " images loaded")
            self.horizontalSlider.setRange(0, numberOfImagesWithLabels - 1)
            self.horizontalSlider.valueChanged.connect(self.doSomethingWithSliderValue)
            print(len(LIST_OF_ALL_FRAMES))
            self.updateCurrentImage(LIST_OF_ALL_FRAMES[self.currentIndex])
            self.pushButton_3.clicked.disconnect()
        return

    def pushButton4WasClicked(self):
        if(self.pathToDataset):
            cv2.imwrite(directoryToDumpFiles + "/labelMe_" + '{:05}'.format(self.currentIndex) + ".jpg", LIST_OF_ALL_FRAMES[self.currentIndex])

        return

    def convertCVMatToPixmap(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
        return QPixmap(qImg)


    def updateCurrentImage(self, frame):
        if(self.pathToDataset):

            pixmap = self.convertCVMatToPixmap(frame)
            self.label.setPixmap(pixmap)
            #self.label_2.setText(LIST_O[self.currentIndex])
        return








#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Filter"))
        self.pushButton.setText(_translate("MainWindow", "Previous"))
        self.pushButton_2.setText(_translate("MainWindow", "Next"))
        self.pushButton_3.setText(_translate("MainWindow", "Load Dataset"))
        self.label_4.setText(_translate("MainWindow", "File Name:"))
        self.label_5.setText(_translate("MainWindow", "Number Of Images In Dataset:"))
        self.pushButton_4.setText(_translate("MainWindow", "SAVE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())