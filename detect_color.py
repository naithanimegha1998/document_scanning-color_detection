import cv2
import numpy as np


def temp(n):
    pass


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 480, 240)
# To extract the values of Hue , Saturation And Value for specific color
cv2.createTrackbar("min hue", "TrackBars", 3, 179, temp)
cv2.createTrackbar("max hue", "TrackBars", 100, 179, temp)
cv2.createTrackbar("min sat", "TrackBars", 64, 255, temp)
cv2.createTrackbar("max sat", "TrackBars", 224, 255, temp)
cv2.createTrackbar("min val", "TrackBars", 223, 255, temp)
cv2.createTrackbar("max val", "TrackBars", 255, 255, temp)

while True:
    img = cv2.imread("Resources/minion.jpg")
    img=cv2.resize(img,(300,300))
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("min hue", "TrackBars")
    h_max = cv2.getTrackbarPos("max hue", "TrackBars")
    s_min = cv2.getTrackbarPos("min sat", "TrackBars")
    s_max = cv2.getTrackbarPos("max sat", "TrackBars")
    v_min = cv2.getTrackbarPos("min val", "TrackBars")
    v_max = cv2.getTrackbarPos("max val", "TrackBars")
    #print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    mask=cv2.resize(mask,(300,300))
    #cv2.imshow("HSV", imgHSV)
    cv2.imshow("Mask ", mask)
    cv2.imshow("Pickachu", img)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    imgResult=cv2.resize(imgResult,(300,300))
    cv2.imshow("Image Result", imgResult)
    cv2.waitKey(1)
