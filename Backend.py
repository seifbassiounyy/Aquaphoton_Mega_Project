import cv2
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Detectiondialog import Ui_Dialog
from GUIFrontend import Ui_MainWindow
from DetectionBCK import FD_GUI


class first_GUI(QMainWindow):
    def __init__(self):
        super(first_GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.detect.clicked.connect(self.Detect)
        self.setconnectivity(60)

    def setconnectivity(self, value):
        x = value / 100
        y = int(x * 201)
        self.ui.hide.setGeometry(QtCore.QRect(0 + y, 0, 201 - y, 50))

    def Detect(self):
        self.detect = FD_GUI()
        self.detect.show()

##

class FD_GUI(QDialog):
    def __init__(self):
        super(FD_GUI, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.cam = CamThread()
        self.cam.start()
        self.cam.video.connect(self.imageupdateslot)
        self.ui.Capture.clicked.connect(self.screenshot)
        self.ui.Exit.clicked.connect(self.exit)

    def exit(self):
        #self.cam.cameraon = False
        self.hide()
        self.cam.stop()


    def screenshot(self):
        pic = self.cam.capture.read()[1]
        cv2.imshow("screenshot", pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def imageupdateslot(self, Image):
        self.ui.Image.setPixmap(QPixmap.fromImage(Image))


class CamThread(QThread):
    video = pyqtSignal(QImage)
    def run(self):
        self.cameraon = True
        self.capture = cv2.VideoCapture(0)
        while self.cameraon:
            ret, frame = self.capture.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flipimg = cv2.flip(img, 1)
                converimg = QImage(flipimg.data, flipimg.shape[1], flipimg.shape[0], QImage.Format_RGB888)
                pic = converimg.scaled(640, 480, Qt.KeepAspectRatio)
                self.video.emit(pic)

    def stop(self):
        self.capture.release()
        self.cameraon = False





##
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    first_ui = first_GUI()
    first_ui.show()
    sys.exit(app.exec())
