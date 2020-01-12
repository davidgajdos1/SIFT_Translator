""" IMPLEMENTACIA GAUSSOVSKEHO ROZOSTRENIA """
import matplotlib.pyplot as pyplot
import scipy
import scipy.ndimage
import numpy as np
from PIL import Image

pyplot.close('all')

def Gaussian_filter(gaussian_blur_sigma,gaussian_blur_kernel_half_width):
#    gaussian_blur_kernel_width      = np.int32(9)
    #gaussian_blur_kernel_half_width = np.int32(4)
    #gaussian_blur_sigma             = np.float32(2)
    'matice gaussovskeho filtra'
    y, x = \
        scipy.mgrid[-gaussian_blur_kernel_half_width:gaussian_blur_kernel_half_width+1,
                    -gaussian_blur_kernel_half_width:gaussian_blur_kernel_half_width+1]
    'ziskanie gaussovskeho kernelu'
    gaussian_blur_kernel_not_normalized = np.exp( ( - ( x**2 + y**2 ) ) / ( 2 * gaussian_blur_sigma**2 ) )
    normalization_constant              = np.float32(1) / np.sum(gaussian_blur_kernel_not_normalized)
    gaussian_blur_kernel                = (normalization_constant * gaussian_blur_kernel_not_normalized).astype(np.float32)
    'zobrazenie gaussovskeho kernelu'
#    pyplot.figure()
#    pyplot.imshow(gaussian_blur_kernel, cmap="gray", interpolation="nearest");
#    pyplot.title("gaussian_blur_kernel");
#    pyplot.colorbar();
    
    return gaussian_blur_kernel

def Gaussian_blur(input_img,convolution_filter,oktava,faktor_rozmazania,kresli,grayscale):
    if not grayscale:
        'preformatovanie obrazka do pola'
        image_array_rgb = np.array(input_img)
        'ziskanie jednotlivych spektier r,g,b,a zo vstupneho obrazka'
        r_spect,g_spect,b_spect = np.split(image_array_rgb, 3, axis=2)
        'aplikacia gaussovskeho filtra na spektra a ulozenie rozostreneho obrazka'
        r_blurred_cpu_gaussian    = scipy.ndimage.filters.convolve(r_spect, np.expand_dims(convolution_filter, axis=0), mode="nearest")
        g_blurred_cpu_gaussian    = scipy.ndimage.filters.convolve(g_spect, np.expand_dims(convolution_filter, axis=0), mode="nearest")
        b_blurred_cpu_gaussian    = scipy.ndimage.filters.convolve(b_spect, np.expand_dims(convolution_filter, axis=0), mode="nearest")
        blurred_cpu_gaussian = np.dstack((r_blurred_cpu_gaussian,g_blurred_cpu_gaussian,b_blurred_cpu_gaussian)).copy()
        'zobrazenie obrazka po konvolucii'
        if kresli:
            pyplot.figure()
            pyplot.imshow(blurred_cpu_gaussian);
            pyplot.title("RGB Gaussian blur "+str(faktor_rozmazania)+" stupna na "+str(oktava)+" oktave");
        
        return blurred_cpu_gaussian[:,:,0:3]
    else:
        blurred_cpu_gaussian = scipy.ndimage.filters.convolve(input_img, convolution_filter, mode="nearest")
        'zobrazenie obrazka po konvolucii'
        if kresli:
            pyplot.figure()
            pyplot.imshow(blurred_cpu_gaussian, cmap='gray', vmin=0, vmax=255)
            pyplot.title("Gray Gaussian blur "+str(faktor_rozmazania)+" stupna na "+str(oktava)+" oktave");
        
        return blurred_cpu_gaussian

def Downsize_img_to_half(im,resize_factor = 1):
    ds_img = im
    half_size = round(max(ds_img.size[0], ds_img.size[1])/resize_factor)
    ds_img.thumbnail((half_size,half_size), Image.ANTIALIAS)
    return ds_img
    
def Create_Octave_Pyramid(img_to_downsize,img,pocet_oktav,preskoc_oktavy,blur_levels,gauss_filter,downscale_factor,kresli,grayscale):
    octaves = []
    octaves_difference_of_gaussians = []
    blurred_cpu_gaussian = img
    oktava_count = 1
    for octave in range(pocet_oktav):
        if oktava_count > preskoc_oktavy:
            blur_factors = []
            difference_of_gaussians = []
            blur_factors.append(blurred_cpu_gaussian)
            if kresli:
                pyplot.figure()
                if not grayscale:
                        pyplot.imshow(blurred_cpu_gaussian)
                else:
                    pyplot.imshow(blurred_cpu_gaussian, cmap='gray', vmin=0, vmax=255)
                pyplot.title("povodny obrazok "+str(octave)+". oktavy");
            for blur_factor in range(blur_levels):
                'ziskanie rozostreneho obrazka'
                blurred_cpu_gaussian = Gaussian_blur(blurred_cpu_gaussian,gauss_filter,octave,blur_factor,kresli,grayscale)
                blur_factors.append(blurred_cpu_gaussian)
                difference_of_gaussians.append(blur_factors[-2]-blur_factors[-1])
                if kresli:
                    pyplot.figure()
                    if not grayscale:
                        pyplot.imshow(difference_of_gaussians[-1])
                    else:
                        pyplot.imshow(difference_of_gaussians[-1], cmap='gray', vmin=0, vmax=255)
                    pyplot.title("DoG medzi "+str(blur_factor)+" a "+str(blur_factor+1)+" stupnom rozmazania"+" na "+str(octave)+". oktave");
            octaves.append(blur_factors); octaves_difference_of_gaussians.append(difference_of_gaussians)
        img_downsized = Downsize_img_to_half(img_to_downsize,downscale_factor)
        blurred_cpu_gaussian = img_downsized
        oktava_count += 1
    
    return octaves,octaves_difference_of_gaussians
