import numpy as np
import cv2
import glob

Paths = glob.glob('Images/*.jpg')
Images = []

for i in Paths:
    print(i)
    img = cv2.imread(i)
    Images.append(img)

Stitch = cv2.Stitcher_create()

error, output = Stitch.stitch(Images)


resized = cv2.resize(output, (int(output.shape[1]/50), int(output.shape[0])), cv2.INTER_AREA)

if error == 0:
    cv2.imshow("Stitched", output)
    cv2.waitKey(0)

output = cv2.copyMakeBorder(output, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)[1]
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
blank = np.zeros(thresh.shape, dtype='uint8')

MaxFrame = max(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(MaxFrame)

cv2.rectangle(blank, (x, y), (x + w, y + h), 255, -1)


cv2.imshow("FRAME", blank)
cv2.waitKey(0)

