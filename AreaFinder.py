"""this module finds areas of image, it first finds edges in picture's pixel area.
 then it makes contours of those edges, and draws biggest contours"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
def smartSelectFunc(filepath):
    #load image to analyze
    img = cv2.imread(filepath,0)

    #find edges, sample picure and min, max values for treshold
    edges = cv2.Canny(img,200,210)

    #find contours from image edges, note find contour destroys original sample variable, so use copy of it
    (_,contours, _) = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    #find biggest contour
    #loop through all contours and find which has most points
    biggestContourLen=0
    biggestContour=0
    for i in range (len(contours)):
        if len(contours[i]) > biggestContourLen:
            biggestContourLen=len(contours[i])
            biggestContour=i
    print(biggestContour)
    print(biggestContourLen)
    print(contours[biggestContour].ndim)
    print(contours[biggestContour].size)
    print(contours[biggestContour])

    #draw original picture and biggest contour on it
    img = cv2.imread(filepath,-1)
    cv2.drawContours(img, contours, biggestContour, (0,255,0,), 3)
    return img
    #cv2.imshow('image', img)
    #cv2.waitKey(0)
#plt.subplot(121),plt.imshow(img,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])


#plt.show()