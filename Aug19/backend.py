import threading
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from frontend import Ui_MainWindow, Ui_Stereo_vision, Ui_Stitching
import datetime
from stitching import Stitch


class DialogStitch(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog = Ui_Stitching()
        self.dialog.setupUi(self)


class StereoVision(QDialog):
    def __init__(self):
        super().__init__()
        self.dialog2 = Ui_Stereo_vision()
        self.dialog2.setupUi(self)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.connectivity = 100

        self.speed = 50
        self.direction = 180
        self.current = 10
        self.voltage = 5
        self.paths = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cam = CamThread(0)
        self.cam.start()

        self.timer = QTimer(self)
        self.timer.start(5)
        self.timer.timeout.connect(self.show_values)

        self.cam.video.connect(self.image_update_slot)
        self.ui.screenshot.clicked.connect(self.thread_capture)

        self.ui.detect.clicked.connect(self.thread_detect)
        self.ui.stereo.clicked.connect(self.stereo_vision)

    def thread_set_values(self):
        t = threading.Thread(target=self.set_values)
        t.start()

    def thread_show_values(self):
        t = threading.Thread(target=self.show_values)
        t.start()

    def thread_detect(self):
        t = threading.Thread(target=self.detection())
        t.start()

    def show_values(self):
        self.show_current()
        self.show_voltage()
        self.show_speed()
        self.show_direction()
        self.show_connectivity()

    def thread_capture(self):
        t = threading.Thread(target=self.capture)
        t.start()

    def capture(self):
        pic = self.cam.capture.read()[1]
        pic = cv2.flip(pic, 1)
        name = str(datetime.datetime.now())
        name = name.replace(':', '-') + '.png'
        cv2.imwrite(name, pic)
        cv2.imshow('screenshot', pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detection(self):
        dialog1.show()
        dialog1.dialog.uploadButton.clicked.connect(self.thread_get_files)
        dialog1.dialog.stitchButton.clicked.connect(self.thread_stitch)

    def thread_get_files(self):
        t = threading.Thread(target=self.get_files)
        t.start()

    def get_files(self):
        self.paths = QFileDialog.getOpenFileNames(filter="Image files (*.jpg *.gif *.png *.jfif *.jpeg)")[0]
        length = len(self.paths)
        dialog1.dialog.uploaded.setText('Uploaded ' + str(length) + ' files')

    def thread_stitch(self):
        t = threading.Thread(target=self.stitch)
        t.start()

    def stitch(self):
        stitch = Stitch()
        name = stitch.stitching(self.paths)
        pixmap = QPixmap(name)
        dialog1.dialog.stitchedLabel.setPixmap(pixmap)

    def stereo_vision(self):
        dialog2.show()

    def image_update_slot(self, image):
        self.ui.camera.setPixmap(QPixmap.fromImage(image))

    def set_values(self):
        pass

    def show_speed(self):
        if self.speed > 100:
            self.speed = 100

        ratio = self.speed / 208
        stylesheet = """border-radius: 150px; background-color: qconicalgradient(cx:0.5, cy:0.5, angle:0, 
        stop:{stop1} rgba(0, 0, 255, 0), stop:{stop2} rgba(0, 0, 255, 255), stop:{stop3} rgba(0, 0, 255, 255), 
        stop:{stop4} rgba(0, 0, 255, 0)); """

        stop4 = 0.5 - ratio
        stop3 = stop4 - 0.001
        stop2 = stop4 - 0.02
        stop1 = stop4 - 0.021

        new_stylesheet = stylesheet.replace('{stop1}', str(stop1)).replace('{stop2}', str(stop2)).replace(
            '{stop3}', str(stop3)).replace('{stop4}', str(stop4))

        self.ui.speedPointer.setStyleSheet(new_stylesheet)

    def show_direction(self):
        self.ui.direction.setValue(self.direction)

    def show_voltage(self):
        self.ui.voltage.display((str(self.voltage)))

    def show_current(self):
        self.ui.current.display(str(self.current))

    def show_connectivity(self):
        if self.connectivity > 100:
            self.connectivity = 100
        ratio = self.connectivity / 100
        x = int(ratio * 201)
        self.ui.hide.setGeometry(QRect(x, 0, 201 - x, 50))


class CamThread(QThread):
    video = pyqtSignal(QImage)

    def __init__(self, v):
        super().__init__()
        self.capture = None
        self.camera_on = True
        self.cam_number = v

    def run(self):
        self.capture = cv2.VideoCapture(self.cam_number)
        while self.camera_on:
            ret, frame = self.capture.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip_img = cv2.flip(img, 1)
                convert_img = QImage(flip_img.data, flip_img.shape[1], flip_img.shape[0], QImage.Format_RGB888)
                pic = convert_img.scaled(640, 480, Qt.KeepAspectRatio)
                self.video.emit(pic)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    dialog1 = DialogStitch()
    dialog2 = StereoVision()
    sys.exit(app.exec())
