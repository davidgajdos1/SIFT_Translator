# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 20:01:19 2019

1. subpixels
2.throw out below treshold
3. eliminate edges


@author: Richard
"""      

def localize_keypoint(D_prev, D_cur, D_next, x, y, np, LA):
      dx = (D_cur[x+1][y]-D_cur[x-1][y])/2. 
      dy = (D_cur[x,y+1]-D_cur[x,y-1])/2. 
      ds = (D_next[x,y]-D_prev[x,y])/2. 
      dxx = D_cur[x+1,y]-2*D_cur[x,y]+D_cur[x-1,y] 
      dxy = ((D_cur[x+1,y+1]-D_cur[x+1,y+1]) - (D_cur[x+1,y-1]-D_cur[x-1,y-1]))/4. 
      dxs = ((D_next[x+1,y]-D_next[x-1,y]) - (D_prev[x+1,y]-D_prev[x-1,y]))/4. 
      dyy = D_cur[x,y+1]-2*D_cur[x,y]+D_cur[x,y-1] 
      dys = ((D_next[x,y+1]-D_next[x,y-1]) - (D_prev[x,y+1]-D_prev[x,y-1]))/4. 
      dss = D_next[x,y]-2*D_cur[x,y]+D_prev[x,y] 
      J = np.array([dx, dy, ds]) 
      HD = np.array([ [dxx, dxy, dxs], [dxy, dyy, dys], [dxs, dys, dss]]) 
      
      offset = -LA.inv(HD).dot(J)
      return offset, J, HD[:2,:2], x, y

def preprocessing_subpixels(difference_of_gaussians_pyramid,extremes_pyramid,np,LA):    
    new_extremes_pyramid = []        
        
    for i in range(0,int(len(difference_of_gaussians_pyramid))): #pocet oktav                       
        D = difference_of_gaussians_pyramid[i]
        new_extremes_pyramid.append([])

        for rr in range(0, int(len(difference_of_gaussians_pyramid))-2): #pocet trojic
            new_extremes_pyramid[i].append([])
            P = len(extremes_pyramid[i][rr])
            for p in range(0,P):#pocet extremov
                
                x = int(extremes_pyramid[i][rr][p][0])
                y = int(extremes_pyramid[i][rr][p][1])
                jas = int(extremes_pyramid[i][rr][p][2])
                
                s=rr+1
                D_prev, D_cur, D_next = D[s-1], D[s], D[s+1]
                offset, J, H, x, y = localize_keypoint(D_prev, D_cur, D_next, x, y, np, LA)
                
                t_c=0.03
                R_th=((10+1)*(10+1))/2
                
                contrast = D[s][x][y] + .5*J.dot(offset)
                if abs(contrast) < t_c: continue
        
                w, v = LA.eig(H)
                r = w[1]/w[0]
                R = (r+1)**2 / r
                if R > R_th: continue
                                
            
                #extremes_pyramid[i][rr][p][0] = x + offset[0]
                #extremes_pyramid[i][rr][p][1] = y + offset[1]
                #extremes_pyramid[i][rr][p][2] += offset[2]
                
                kp = np.array([x + offset[0], y + offset[1], jas + offset[2]])
                if kp[0] >= len(D[0]) or kp[1] >= len(D[0][0]): continue # throw out boundary points because I don't want to deal with them

                new_extremes_pyramid[i][rr].append(kp);
    
    return new_extremes_pyramid