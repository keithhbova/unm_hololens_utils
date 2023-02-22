# Form implementation generated from reading ui file 'webcam.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog
from pathlib import Path
import os
import sys
import cv2
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import subprocess

CURRENT_PATH = os.getcwd()
TEMP_FILE_NAME = CURRENT_PATH + "/test.avi"

OPENCV_CAMERA_INDEX = 1


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = False

    def run(self):
        # capture from web cam
        self._run_flag = True
        cap = cv2.VideoCapture(0)
        frameWidth = int(cap.get(3))
        frameHeight = int(cap.get(4))
        fps = 9
        
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        
        videoOut = cv2.VideoWriter(TEMP_FILE_NAME,fourcc, fps, (frameWidth,frameHeight), 3)
        
        #videoOut = cv2.VideoWriter(TEMP_FILE_NAME,fourcc, fps, (frameWidth,frameHeight), 3)

        #videoOut = cv2.VideoWriter(TEMP_FILE_NAME, fourcc, 20.0, (640, 480), 0)
        
        while self._run_flag:
            ret, cv_img = cap.read()
            #cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            videoOut.write(cv_img)
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()
        videoOut.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
        
        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(674, 644)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 641, 481))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 550, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 550, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 674, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   


        self.label.setScaledContents(True)
        self._cameraIsRecording = False
        #self.disply_width = 640
        #self.display_height = 480
        
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        #self.thread.start()
        self.pushButton.clicked.connect(self.pushButton1WasClicked)
        self.pushButton_2.clicked.connect(self.pushButton2WasClicked)
        
    def pushButton1WasClicked(self):
        if(not self._cameraIsRecording):
            self._cameraIsRecording = True
            self.thread.start()
        return
        
    def pushButton2WasClicked(self):
        if(self._cameraIsRecording):
            self._cameraIsRecording = False
            self.thread.stop()
            home_dir = str(Path.home())
            qfd = QFileDialog()
            fileName = qfd.getSaveFileName(qfd, 'Open file', home_dir)[0]
            self.moveSavedAviToLocationDeleteAndChangeName(fileName)
        return
            

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def moveSavedAviToLocationDeleteAndChangeName(self, newFileName):
        if(newFileName):
            if(newFileName.endswith(".avi")):
                subprocess.call("mv " + str(TEMP_FILE_NAME) + " " + str(newFileName) , shell=True)
            subprocess.call("mv " + str(TEMP_FILE_NAME) + " " + str(newFileName) + ".avi" , shell=True)
        return
        

    #@pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        #p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap(convert_to_Qt_format)











#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Flir Capture"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())