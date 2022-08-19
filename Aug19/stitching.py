import numpy as np
import cv2
import datetime


class Stitch:
    def stitching(self, paths):
        images = []
        for i in paths:
            img = cv2.imread(i)
            images.append(img)

        Stitch = cv2.Stitcher_create()
        error, output = Stitch.stitch(images)

        output = cv2.copyMakeBorder(output, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))

        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blank = np.zeros(thresh.shape, dtype='uint8')

        MaxFrame = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(MaxFrame)

        cv2.rectangle(blank, (x, y), (x + w, y + h), 255, -1)

        minimum = blank.copy()
        sub = blank.copy()

        while cv2.countNonZero(sub) > 0:
            minimum = cv2.erode(minimum, None)
            sub = cv2.subtract(minimum, thresh)

        contours, _ = cv2.findContours(minimum, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        MaxFrame = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(MaxFrame)

        output = output[y:y + h, x:x + w]
        resized = cv2.resize(output, (int(output.shape[1] / 4), int(output.shape[0] / 4)), cv2.INTER_AREA)
        name = str(datetime.datetime.now())
        name = name.replace(':', '-') + '.png'
        cv2.imwrite(name, resized)
        return name
