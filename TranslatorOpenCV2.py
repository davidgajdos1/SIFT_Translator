# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 12:35:30 2020

@author: Ranger
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 5

#initiate camera
camera = cv2.VideoCapture(0)

#camera resolution settings
camera.set(3, 480) #vertical pixels
camera.set(4, 640) #horizontal pixels

#img1 = cv2.imread('train.jpg',0)          # queryImage
img2 = cv2.imread('train.jpg',0) # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create(nfeatures = 0,
                            		nOctaveLayers = 5,
                            		contrastThreshold = 0.04,
                            		edgeThreshold = 10,
                            		sigma = 1.2 )

# find the keypoints and descriptors with SIFT
#kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

while (True):
    check, frame = camera.read()
    img1 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    kp1, des1 = sift.detectAndCompute(img1,None)

    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    matchesMask = [[0,0] for i in range(len(matches))]
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
            good.append(m)
            
    dst_pt = [ kp2[m.trainIdx].pt for m in good ] 
    print(dst_pt)
    
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
    
        if(M is not None):        
            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)
    
            #img2 = cv2.polylines(img2,[np.int32(dst)],True,0,2, cv2.LINE_AA)
    
    else:
        #print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
        matchesMask = None
        
    draw_params = dict(matchColor = (255,0,0), # draw matches in red color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    
    cv2.imshow('result',img3)
       
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.waitKey()
