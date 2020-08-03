import cv2
import numpy as np

width_img=480
height_img=550

def preProcessing(img):
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlurr=cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny=cv2.Canny(imgBlurr,150,150)
    kernel=np.ones((5,5))
    imgDial=cv2.dilate(imgCanny, kernel,iterations=2)
    imgErode=cv2.erode(imgDial,kernel,iterations=1)

    return imgErode

def getContours(img):
    biggest= np.array([])
    maxArea=0
    contours, hr=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        #print(area)
        if area>5000:   ##filtering for largest shape in image
            #cv2.drawContours(imgcontour,cnt,-1,(255,255,0),4)
            peri=cv2.arcLength(cnt,True) ## to find object of 4 sides
            approx=cv2.approxPolyDP(cnt,0.02*peri,True) ##store corner points of shape
            #print(approx)
            if area>maxArea and  len(approx)==4:
                biggest=approx
                maxArea=area
            #cv2.drawContours(imgcontour,biggest,-1,(255,0,255),8)
    return biggest

def reorder(biggest):
    biggest=biggest.reshape((4,2))
    biggestnew= np.zeros((4,1,2),np.int32)
    add=biggest.sum(1)
    biggestnew[0]=biggest[np.argmin(add)]
    biggestnew[3] = biggest[np.argmax(add)]
    diff=np.diff(biggest, axis=1)
    biggestnew[1]=biggest[np.argmin(diff)]
    biggestnew[2] = biggest[np.argmax(diff)]
    print(biggestnew)
    return biggestnew


def getWarp(img,biggest):
    print(biggest)
    biggest=reorder(biggest)
    pt1=np.float32(biggest)
    pt2=np.float32([[0,0],[width_img,0],[0,height_img],[width_img,height_img]])
    matrix=cv2.getPerspectiveTransform(pt1,pt2)
    imgOutput=cv2.warpPerspective(img, matrix,(width_img,height_img))
    imgOutput=imgOutput[10:-50,10:-60]
    return imgOutput


img = cv2.imread("Resources/document4.jpg")  # your document to be scanned 
img = cv2.resize(img, (width_img, height_img))
imgResult= img.copy()
imgpreprocces=preProcessing(imgResult)
biggestcontour= getContours(imgpreprocces)
cv2.drawContours(imgResult, biggestcontour, -1, (255, 0, 255), 8)
#print(len(biggestcontour))
imgWarped=getWarp(imgResult,biggestcontour)
#cv2.imshow("Pre Processed ",imgpreprocces )
#cv2.imshow("image Contour", imgResult)
cv2.imshow("Image ", img)
cv2.imshow(" warped", imgWarped)
#hstak=np.hstack((imgWarped,imgResult))
#cv2.imshow("Warped Image", hstak)
cv2.waitKey(0)