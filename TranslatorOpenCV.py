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
camera.set(2, 1)

train = cv.imread('train.jpg',cv.IMREAD_GRAYSCALE) # trainImage
# Initiate SIFT detector, parameter explaination at https://docs.opencv.org/3.4/d5/d3c/classcv_1_1xfeatures2d_1_1SIFT.html
sift = cv.xfeatures2d.SIFT_create(nfeatures = 0,
                            		nOctaveLayers = 5,
                            		contrastThreshold = 0.04,
                            		edgeThreshold = 10,
                            		sigma = 1.6 )
MIN_MATCH_COUNT = 3
# find the keypoints and descriptors with SIFT
kp2, des2 = sift.detectAndCompute(train,None)
# BFMatcher with default params
bf = cv.BFMatcher()

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv.FlannBasedMatcher(index_params, search_params)

#cv.imshow("result",img3)
#cv.waitKey()

while (True):
    check, frame = camera.read()
    frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    #cv2.rectangle(frame, (300,300), (50,50), (0,0,255),3)
    #croped_frame = frame[50:300, 50:300]
 
    
    #cv.imshow('img',frame)  
    kp1, des1 = sift.detectAndCompute(frame,None)
    #matches = bf.knnMatch(des1,des2,k=2)
    
    matches = flann.knnMatch(des1,des2,k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
                
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
    
        h,w = train.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)
    
        frame = cv.polylines(frame,[np.int32(dst)],True,255,3, cv.LINE_AA)

    else:
        print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None    

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = cv.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)

    img3 = cv.drawMatches(frame,kp1,train,kp2,good,None, **draw_params)
    #img3 = cv.drawMatchesKnn(frame,kp1,train,kp2,good,None,flags=cv.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    cv.imshow('result',img3)  
   
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
 
cv.waitKey(0)