"""
IMPORTANT IMPORTS
"""

'kniznice'
import matplotlib.pyplot as pyplot
from PIL import Image
import numpy as np
import time
from numpy import linalg as LA
import copy
'vlastne importy'
from Octaves import Create_Octave_Pyramid,Gaussian_filter
from Keypoints import Detect_Extremes
from keypoint_localization import localize_keypoint, preprocessing_subpixels
from oriental import assign_orientation_all
'timer start'
start = time.time()

"""
SIFT IMPLEMENTATION FOR LETTER RECOGNITION
"""

'parametre pre vytvorenie oktav'
pocet_oktav = 4; preskoc_oktavy = 0
blur_levels = 4 # 1 + blur_levels obrazkov v oktave, -1 obrazkov mas v dog
downscale_factor = 2
sigma = 1.6
kernel_half_size = 4
kresli = 0
grayscale = 1
'nacitanie obrazka'
if not grayscale:
    img = Image.open("C:/Users/Ranger/Desktop/SKOLA/PV2/cat.jpg")
else:
    img = Image.open("C:/Users/Ranger/Desktop/SKOLA/PV2/cat.jpg").convert('L')
'vytvorenie kopie pre down-scaling'
img_to_downsize = img.copy()
'zobrazenie povodneho obrazka'
#pyplot.figure()
#if not grayscale:
#    pyplot.imshow(img)
#else:
#    pyplot.imshow(img, cmap='gray', vmin=0, vmax=255)
#pyplot.title("povodny_obrazok");
'toto pouzijem ak chcem zaporne hodnoty pri diferenciach gausianov'
#img = np.int16(img);
'ziskanie gaussovskeho filtra'
gaussian_blur_filter = Gaussian_filter(sigma,kernel_half_size)

'ziskanie pyramidy oktav a diferencie gausianov'
octaves_pyramid,difference_of_gaussians_pyramid = Create_Octave_Pyramid(img_to_downsize,img,pocet_oktav,preskoc_oktavy,blur_levels,gaussian_blur_filter,downscale_factor,kresli,grayscale)

'ziskanie pyramidy extremov pre vsetky oktavy'
extremes_pyramid = Detect_Extremes(difference_of_gaussians_pyramid,np)

extremes_pyramid_old = copy.deepcopy(extremes_pyramid)

extremes_pyramid = preprocessing_subpixels(difference_of_gaussians_pyramid,extremes_pyramid,np,LA)
#extremes_pyramid_old = copy.deepcopy(extremes_pyramid)

new_kps_pyramid = assign_orientation_all(extremes_pyramid, difference_of_gaussians_pyramid, num_bins=36)

'timer end'
end = time.time()
print(end - start)
