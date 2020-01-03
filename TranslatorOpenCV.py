# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:09:27 2020

@author: Ranger
"""

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

#initiate camera
camera = cv.VideoCapture(0)

#camera resolution settings
camera.set(3, 480) #vertical pixels
camera.set(4, 640) #horizontal pixels

train = cv.imread('train.jpg',cv.IMREAD_GRAYSCALE) # trainImage
# Initiate SIFT detector, parameter explaination at https://docs.opencv.org/3.4/d5/d3c/classcv_1_1xfeatures2d_1_1SIFT.html
sift = cv.xfeatures2d.SIFT_create(nfeatures = 0,
                            		nOctaveLayers = 5,
                            		contrastThreshold = 0.04,
                            		edgeThreshold = 10,
                            		sigma = 1.6 )

# find the keypoints and descriptors with SIFT
kp2, des2 = sift.detectAndCompute(train,None)
# BFMatcher with default params
bf = cv.BFMatcher()

#cv.imshow("result",img3)
#cv.waitKey()

while (True):
    check, frame = camera.read()
    #cv2.rectangle(frame, (300,300), (50,50), (0,0,255),3)
    #croped_frame = frame[50:300, 50:300]
 
    
    #cv.imshow('img',frame)  
    kp1, des1 = sift.detectAndCompute(frame,None)
    matches = bf.knnMatch(des1,des2,k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])
    # cv.drawMatchesKnn expects list of lists as matches.
    img3 = cv.drawMatchesKnn(frame,kp1,train,kp2,good,None,flags=cv.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    cv.imshow('result',img3)  
   
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
 
cv.waitKey(0)