import cv2
import numpy as np

def detect(img):
    lower = np.array([0, 50, 50])
    upper = np.array([255, 160, 160])

    star_mask = cv2.inRange(img, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 100))
    star_mask = cv2.morphologyEx(star_mask, cv2.MORPH_TOPHAT, kernel)
    #star_mask = cv2.morphologyEx(star_mask, cv2.MORPH_CLOSE, kernel)
    return star_mask


image = cv2.imread('stitched.png')
cv2.imshow('', image)
cv2.waitKey(0)
img = detect(image)
cv2.imshow('', img)
cv2.waitKey(0)
