# Form implementation generated from reading ui file 'labelViewerPostExport.ui'
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
from YOLOv7 import YOLOv7
from YOLOv7 import utils as ut
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path




LIST_OF_ALL_FRAMES_WITH_LABELS = []
LIST_OF_ALL_FILE_NAMES = []


def getALabeledImageFromAName(fileName, pathToDataset):
    
    pathToImage = str(pathToDataset) + "/images/" + str(fileName) + ".jpg"
    pathToLabel = str(pathToDataset) + "/labels/" + str(fileName) + ".txt"

    frame = cv2.imread(pathToImage)
    
    ids, boxes = ut.getIdsAndBoxesFromImageTxt(pathToLabel, frame.shape[1], frame.shape[0])  
    
    newFrame = ut.drawLabelsOnFrame(frame, boxes, ids)
    return newFrame

def loadDatasetIntoMemoryAndDrawLabels(pathToDataset):
    pathToImages = str(pathToDataset) + "/images"
    path = Path(pathToImages).glob('*.jpg')
    listOfFileNames = [str(fileName).replace(".jpg", "").replace(pathToImages, "").replace("/", "") for fileName in path if fileName.is_file()]
    listOfFileNames.sort()
    
    for fileName in listOfFileNames:
        LIST_OF_ALL_FRAMES_WITH_LABELS.append(getALabeledImageFromAName(fileName, pathToDataset))
        LIST_OF_ALL_FILE_NAMES.append(fileName)
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
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 580, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 580, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 550, 491, 20))
        self.label_2.setObjectName("label_2")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(50, 620, 571, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 660, 151, 16))
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

    
                
    def doSomethingWithSliderValue(self, value):
        self.currentIndex = value
        self.updateCurrentImage(LIST_OF_ALL_FRAMES_WITH_LABELS[self.currentIndex])
        return     
        
        
        
    def pushButton1WasClicked(self):
        if(self.pathToDataset):
            if(self.currentIndex - 1 >= 0):
                self.currentIndex -= 1
                self.updateCurrentImage(LIST_OF_ALL_FRAMES_WITH_LABELS[self.currentIndex])
        return
    
    def pushButton2WasClicked(self):
        if(self.pathToDataset):
            if(self.currentIndex + 1 < len(LIST_OF_ALL_FRAMES_WITH_LABELS)):
                self.currentIndex += 1
                self.updateCurrentImage(LIST_OF_ALL_FRAMES_WITH_LABELS[self.currentIndex])
        return
    
        
    def pushButton3WasClicked(self):
        homeDir = str(Path.home())
        qfd = QFileDialog()
        self.pathToDataset = str(QFileDialog.getExistingDirectory(qfd ,"Select Directory", homeDir))
        if(self.pathToDataset):
            loadDatasetIntoMemoryAndDrawLabels(self.pathToDataset)
            numberOfImagesWithLabels = len(LIST_OF_ALL_FRAMES_WITH_LABELS)
            self.label_3.setText(str(numberOfImagesWithLabels) + " images loaded")
            self.horizontalSlider.setRange(0, numberOfImagesWithLabels - 1)
            self.horizontalSlider.valueChanged.connect(self.doSomethingWithSliderValue)
            self.updateCurrentImage(LIST_OF_ALL_FRAMES_WITH_LABELS[self.currentIndex])
            self.pushButton_3.clicked.disconnect()
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
            self.label_2.setText(LIST_OF_ALL_FILE_NAMES[self.currentIndex])
        return


    





#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yolo Dataset Viewer"))
        self.label.setText(_translate("MainWindow", " "))
        self.pushButton.setText(_translate("MainWindow", "Previous"))
        self.pushButton_2.setText(_translate("MainWindow", "Next"))
        self.label_2.setText(_translate("MainWindow", "  "))
        self.label_3.setText(_translate("MainWindow", "  "))
        self.pushButton_3.setText(_translate("MainWindow", "Load Dataset"))
        self.label_4.setText(_translate("MainWindow", "File Name:"))
        self.label_5.setText(_translate("MainWindow", "Number Of Images In Dataset:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
