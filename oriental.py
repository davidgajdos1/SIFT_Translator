# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:18:30 2019

@author: Richard
"""

import numpy as np
from numpy import linalg as LA
from Octaves import Gaussian_filter

from gaussian_filter import gaussian_filter

def cart_to_polar_grad(dx, dy):
    m = np.sqrt(dx**2 + dy**2)
    theta = (np.arctan2(dx, dy)+np.pi) * 180/np.pi
    return m, theta

def get_grad(L, x, y):
    dy = L[x,min(L.shape[1]-1, y+1)] - L[x,max(0, y-1)]
    dx = L[min(L.shape[0]-1, x+1),y] - L[max(0, x-1),y]
    return cart_to_polar_grad(dx, dy)

def quantize_orientation(theta, num_bins):
    bin_width = 360//num_bins
    return int(np.floor(theta)//bin_width)

def fit_parabola(hist, binno, bin_width):
    centerval = binno*bin_width + bin_width/2.

    if binno == len(hist)-1: rightval = 360 + bin_width/2.
    else: rightval = (binno+1)*bin_width + bin_width/2.

    if binno == 0: leftval = -bin_width/2.
    else: leftval = (binno-1)*bin_width + bin_width/2.
    
    A = np.array([
        [centerval**2, centerval, 1],
        [rightval**2, rightval, 1],
        [leftval**2, leftval, 1]])
    b = np.array([
        hist[binno],
        hist[(binno+1)%len(hist)], 
        hist[(binno-1)%len(hist)]])

    x = LA.lstsq(A, b, rcond=None)[0]
    if x[0] == 0: x[0] = 1e-6
    return -x[1]/(2*x[0])

def assign_orientation(kps, octave, num_bins=36):
    new_kps = []
    bin_width = 360//num_bins
   
    
    
    for kp in kps:
        cx, cy, s = int(kp[0]), int(kp[1]), int(kp[2])
        s = np.clip(s, 0, len(octave)-1)

        sigma = kp[2]*1.5
        w = int(2*np.ceil(sigma)+1)
        kernel = gaussian_filter(sigma)

        #L = octave[...,s]
        L=octave[s]
        hist = np.zeros(num_bins, dtype=np.float32)

        for oy in range(-w, w+1):
            for ox in range(-w, w+1):
                x, y = cx+ox, cy+oy
                
                if x < 0 or x >= len(octave[0])-1: continue
                elif y < 0 or y >= len(octave[0][0])-1: continue
                
                m, theta = get_grad(L, x, y)
                weight = kernel[oy+w, ox+w] * m

                bin = quantize_orientation(theta, num_bins)
                hist[bin] += weight

        max_bin = np.argmax(hist)
        new_kps.append([kp[0], kp[1], kp[2], fit_parabola(hist, max_bin, bin_width)])

        max_val = np.max(hist)
        for binno, val in enumerate(hist):
            if binno == max_bin: continue

            if .8 * max_val <= val:
                new_kps.append([kp[0], kp[1], kp[2], fit_parabola(hist, binno, bin_width)])

    return np.array(new_kps)

def assign_orientation_all(extremes_pyramid, difference_of_gaussians_pyramid, num_bins=36):
    new_kps_pyramid = []
    for i in range(0,len(difference_of_gaussians_pyramid)-1):
        new_kps_pyramid.append([])
        for j in range(0,1):
            new_kps_pyramid[i].append([])
            new_kps_array = assign_orientation(extremes_pyramid[i][j], difference_of_gaussians_pyramid[i], num_bins=36)
            new_kps_pyramid[i][j].append(new_kps_array)
    
    return new_kps_pyramid



def orientations(octaves,extremes):
    fis_pyramid = []
    for i in range(0,len(octaves)):
        fi = []
        img_array = np.asarray(octaves[i][0])
        for extreme in extremes[i][0]:
            ex = extreme
            l1 = img_array[int(ex[0])+1,int(ex[1])]
            l2 = img_array[int(ex[0])-1,int(ex[1])]
            l3 = img_array[int(ex[0]),int(ex[1])+1]
            l4 = img_array[int(ex[0]),int(ex[1])-1]
            #mag =  np.sqrt(np.power(l1-l2,2) + np.power(l3-l4,2))
            fi.append(np.arctan((l3-l4)/(l1-l2)))
        fis_pyramid.append(fi)
    return fis_pyramid
