# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:12:47 2019

@author: Ranger
"""

def cart_to_polar_grad(dx, dy): 
  m = np.sqrt(dx**2 + dy**2) 
  theta = (np.arctan2(dy, dx)+np.pi) * 180/np.pi 
  return m, theta 

def get_grad(L, x, y): 
  dy = L[min(L.shape[0]-1, y+1),x] — L[max(0, y-1),x] 
  dx = L[y,min(L.shape[1]-1, x+1)] — L[y,max(0, x-1)] 
  return cart_to_polar_grad(dx, dy)

def quantize_orientation(theta, num_bins): 
  bin_width = 360//num_bins 
  return int(np.floor(theta)//bin_width)

def get_patch_grads(p): 
  r1 = np.zeros_like(p) 
  r1[-1] = p[-1] 
  r1[:-1] = p[1:]   r2 = np.zeros_like(p) 
  r2[0] = p[0] 
  r2[1:] = p[:-1]   dy = r1-r2   r1[:,-1] = p[:,-1] 
  r1[:,:-1] = p[:,1:] 
  r2[:,0] = p[:,0] 
  r2[:,1:] = p[:,:-1]   dx = r1-r2   
  return dx, dy
  

def get_histogram_for_subregion(m, theta, num_bin, reference_angle, bin_width, subregion_w): 
  hist = np.zeros(num_bin, dtype=np.float32) 
  c = subregion_w/2 - .5  
  for mag, angle in zip(m, theta):
    angle = (angle-reference_angle) % 360        
    binno = quantize_orientation(angle, num_bin)        
    vote = mag      
   
    hist_interp_weight = 1 - abs(angle - (binno*bin_width + bin_width/2))/(bin_width/2)        
    vote *= max(hist_interp_weight, 1e-6)             
    gy, gx = np.unravel_index(i, (subregion_w, subregion_w))        
    x_interp_weight = max(1 - abs(gx - c)/c, 1e-6)            
    y_interp_weight = max(1 - abs(gy - c)/c, 1e-6)        
    vote *= x_interp_weight * y_interp_weight             
    hist[binno] += vote  hist /= max(1e-6, LA.norm(hist)) 
  hist[hist>0.2] = 0.2 
  hist /= max(1e-6, LA.norm(hist))
  return hist

def get_local_descriptors(kps, octave, np, LA, w=16, num_subregion=4, num_bin=8): 
  descs = [] 
  bin_width = 360//num_bin  
  for kp in kps: 
    cx, cy, s = int(kp[0]), int(kp[1]), int(kp[2]) 
    s = np.clip(s, 0, octave.shape[2]-1) 
    kernel = gaussian_filter(w/6) # gaussian_filter multiplies sigma by 3 
    L = octave[…,s]     t, l = max(0, cy-w//2), max(0, cx-w//2) 
    b, r = min(L.shape[0], cy+w//2+1), min(L.shape[1], cx+w//2+1) 
    patch = L[t:b, l:r] 
    dx, dy = get_patch_grads(patch)     
    if dx.shape[0] < w+1: 
      if t == 0: kernel = kernel[kernel.shape[0]-dx.shape[0]:] 
      else: kernel = kernel[:dx.shape[0]] 
    if dx.shape[1] < w+1: 
      if l == 0: kernel = kernel[kernel.shape[1]-dx.shape[1]:] 
      else: kernel = kernel[:dx.shape[1]] 
    if dy.shape[0] < w+1: 
      if t == 0: kernel = kernel[kernel.shape[0]-dy.shape[0]:] 
      else: kernel = kernel[:dy.shape[0]] 
    if dy.shape[1] < w+1: 
      if l == 0: kernel = kernel[kernel.shape[1]-dy.shape[1]:] 
      else: kernel = kernel[:dy.shape[1]]     
      m, theta = cart_to_polar_grad(dx, dy) 
    dx, dy = dx*kernel, dy*kernel     
    subregion_w = w//num_subregion 
    featvec = np.zeros(num_bin * num_subregion**2, dtype=np.float32)     
    for i in range(0, subregion_w): 
      for j in range(0, subregion_w): 
        t, l = i*subregion_w, j*subregion_w 
        b, r = min(L.shape[0], (i+1)*subregion_w), min(L.shape[1], (j+1)*subregion_w)         
        hist = get_histogram_for_subregion(m[t:b, l:r].ravel(), theta[t:b, l:r].ravel(), num_bin, kp[3], bin_width, subregion_w)         featvec[i*subregion_w*num_bin + j*num_bin:i*subregion_w*num_bin + (j+1)*num_bin] = hist.flatten()     featvec /= max(1e-6, LA.norm(featvec))        
    featvec[featvec>0.2] = 0.2        
    featvec /= max(1e-6, LA.norm(featvec))    
    descs.append(featvec)  
    return np.array(descs)
