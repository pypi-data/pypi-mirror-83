#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:51:15 2018

@author: antony
"""
import numpy as np
from PIL import Image, ImageFilter

NO_COLOR = [0, 0, 0, 0]

def new(w, h):
    """
    Returns a w x h x 4 matrix representing an RGBA image with 4 channels.
    
    Parameters
    ----------
    w : int
        Image width.
    h : int
        Image height.
        
    Returns
    -------
    numpy.array
        w x h x 4 array
    """
    
    return np.full((h, w, 4), NO_COLOR, dtype='uint8') #Image.new('RGBA', (w * 300, w * 300))


def remove_background(im, imout=None, threshold=200):
    im_no_bg = im.copy()
    
    # find gray areas and mask
    r = im_no_bg[:, :, 0]
    g = im_no_bg[:, :, 1]
    b = im_no_bg[:, :, 2]
        
    gray_areas = (r > threshold) & (g > threshold) & (b > threshold)
    #print(gray_areas)
        
    d = im_no_bg[np.where(gray_areas)]
    d[:, :] = NO_COLOR
    im_no_bg[np.where(gray_areas)] = d
    
    if imout is not None:
        imout.paste(imout, im_no_bg, inplace=True)
    
    return im_no_bg


def smooth(im, imout=None):
    im_smooth = np.array(Image.fromarray(im).filter(ImageFilter.SMOOTH).convert('RGBA'))
    
    #im2.paste(im_smooth, (0, 0), im_smooth)
    
    if imout is not None:
        paste(imout, im_smooth, inplace=True)
    
    return im_smooth

def paste(imout, im, offset=(0, 0), inplace=False):
    im1 = Image.fromarray(imout)
    im2 = Image.fromarray(im)
    
    im1.paste(im2, offset, im2)
    
    ret = np.array(im1.convert('RGBA'))

    if inplace:
        imout[:,:] = ret
    
    return ret
    

def edges(im, 
          imout=None,
          rmbg=True,
          color=[0, 0, 0, 255]):
    """
    Run edge detection on image. This method removes light grays
    from the image before doing edge detection on the assumption that gray
    areas represent background and should be discarded.
    
    Parameters
    ----------
    im: PIL.image
        Input image
    imout: PIL.image, optional
        im_smooth will be applied to image if supplied. Default None
    removebg : bool, optional
        Whether to remove background gray pixels. Default True.
        
    Returns
    -------
    im_no_gray : PIL.image
        input image with gray removed
    im_smooth : PIL.image
        smoothed edge detection on input image after possible gray removal
    """
    
    if rmbg:
        im = remove_background(im)

    # Edge detect on what is left (the clusters)
    im_edges = np.array(Image.fromarray(im).filter(ImageFilter.FIND_EDGES).convert('RGBA'))
    
    a = im_edges[:, :, 3]
    
    # anything that isn't transparent, color
    im_edges[np.where(a > 0)] = color

    if imout is not None:
        paste(imout, im_edges, inplace=True)
        
    #save(im_edges, 'edges.png')
    
    return im_edges



def smooth_edges(im, imout=None, rmbg=True):
    """
    Do edge detection and then smooth. This method removes light grays
    from the image before doing edge detection on the assumption that gray
    areas represent background and should be discarded.
    
    Parameters
    ----------
    im: PIL.image
        Input image
    imout: PIL.image, optional
        im_smooth will be applied to image if supplied. Default None
    removebg : bool, optional
        Whether to remove background gray pixels. Default True.
        
    Returns
    -------
    im_no_gray : PIL.image
        input image with gray removed
    im_smooth : PIL.image
        smoothed edge detection on input image after possible gray removal
    """
    
    im_edges = edges(im, rmbg=rmbg)
 
    return smooth(im_edges, imout=imout)

def open(file):
    return np.array(Image.open(file).convert('RGBA'))

def save(im, out):
    ext = out[-3:]
    Image.fromarray(im).save(out, ext)
