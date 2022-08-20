import cv2
import numpy as np
import datetime


def detect(img):
    global image
    image = img.copy()
    img2 = img.copy()
    img3 = img2.copy()
    img4 = img2.copy()
    star(img)
    fragment(img2)
    sponge(img3)
    # colony(img4)
    name = str(datetime.datetime.now())
    name = name.replace(':', '-') + '.png'
    cv2.imwrite(name, image)
    return name


def colony(img):
    lower = np.array([150, 130, 0])
    upper = np.array([200, 200, 255])

    background = cv2.inRange(img, lower, upper)
    cv2.imshow('', background)
    cv2.waitKey(0)
    kernel = np.ones((5, 2), np.uint8)
    background = cv2.erode(background, kernel, iterations=1)

    mask = 255 - background

    cv2.imshow('', mask)
    cv2.waitKey(0)

    img = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('', img)
    cv2.waitKey(0)

    lower = np.array([80, 80, 100])
    upper = np.array([200, 200, 255])

    colony_mask = cv2.inRange(img, lower, upper)
    img = cv2.bitwise_and(img, img, mask=colony_mask)

    cv2.imshow('', colony_mask)
    cv2.waitKey(0)


def sponge(img):
    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])

    sponge_mask = cv2.inRange(img, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 20))
    sponge_mask = cv2.morphologyEx(sponge_mask, cv2.MORPH_CLOSE, kernel)

    edged = cv2.Canny(sponge_mask, 100, 100)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(contours)

    i = 0
    while i < len(contours):
        area = cv2.contourArea(contours[i])
        approx = cv2.approxPolyDP(contours[i], 0.04 * cv2.arcLength(contours[i], True), True)

        if area < 1000 or len(approx) < 4:
            contours.pop(i)

        else:
            i += 1

    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        cv2.rectangle(image, (x, y), (x + w, y + h), (50, 200, 100), 4)
        cv2.putText(image, 'Sponge', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)


def fragment(img):
    lower = np.array([0, 210, 210])
    upper = np.array([255, 255, 255])

    frag_mask = cv2.inRange(img, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
    frag_mask = cv2.morphologyEx(frag_mask, cv2.MORPH_CLOSE, kernel)

    edged = cv2.Canny(frag_mask, 100, 100)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(contours)

    i = 0
    while i < len(contours):
        area = cv2.contourArea(contours[i])
        approx = cv2.approxPolyDP(contours[i], 0.04 * cv2.arcLength(contours[i], True), True)

        if area <= 100 or len(approx) != 4:
            contours.pop(i)

        else:
            i += 1

    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 100, 234), 4)
        cv2.putText(image, 'Coral Fragment', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)


def star(img):
    lower = np.array([170, 100, 100])
    upper = np.array([255, 160, 160])

    star_mask = cv2.inRange(img, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    star_mask = cv2.morphologyEx(star_mask, cv2.MORPH_CLOSE, kernel)

    kernel = np.ones((3, 3), np.uint8)
    star_mask = cv2.erode(star_mask, kernel, iterations=1)
    star_mask = cv2.dilate(star_mask, kernel, iterations=1)

    edged = cv2.Canny(star_mask, 100, 100)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(contours)

    i = 0
    while i < len(contours):
        area = cv2.contourArea(contours[i])
        approx = cv2.approxPolyDP(contours[i], 0.04 * cv2.arcLength(contours[i], True), True)

        if area <= 100 or len(approx) < 4:
            contours.pop(i)

        else:
            i += 1

    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 150, 0), 4)
        cv2.putText(image, 'Sea Star', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)


colony(cv2.imread('stitched.png'))
