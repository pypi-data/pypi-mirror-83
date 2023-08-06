import pytest
from astropy.io import fits
import os
import pandas as pd
import numpy as np
import astropy.convolution as conv
import glob
import pyklip.klip as klip
import pyklip.instruments.MagAO as MagAO
import pyklip.parallelized as parallelized
import pyklip.fakes as fakes
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import shutil
import re
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as patches
from importlib import reload
from datetime import datetime


testdir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

def slicecube(im, rotfile, datadir='./', slicedir='sliced/'):
    """
    This function slices a 3D cube of shape (N, y, x) where N is the number of frames into individual 2D images numbered sequentially. The version in this module is specifically made to test the function's accuracy.
    
    Args:
        im (str): Name of the 3D image
        rotfile (str): Name of the cube containing the rotoff values needed to rotate images
        datadir (str): Directory containing the 3D image. Defaults to './'
        slicedir: Name of the directory to write the sliced images into. Defaults to 'sliced/'

    Returns:
        (list of (np.ndarray)): Array of the shapes of the output files
        (int): Number of files ouput
        (int): Number of files input
        
    """

    # Read in 3D image, header, and rotoffs
    cube = fits.getdata(im)
    header = fits.getheader(im)
    rotoffs = fits.getdata(rotfile)

    # Record image dimensions
    nims, ydim, xdim = cube.shape

    # Check that rotoff and nims dimension are same length
    if nims != len(rotoffs):
        raise IndexError('Number of images and number of rotoffs are not equal')

    # Create sliced directory if doesn't already exist
    if not os.path.exists(datadir+slicedir):
        os.makedirs(datadir+slicedir)

    # Save 2D images in list

    sliced_shape = []
    for i in range(nims):
        sliced_im = cube[i,:,:]
        header["rotoff"]=rotoffs[i]
        sliced_shape.append(sliced_im.shape)
    
    output_len = len(sliced_shape)

    return np.array(sliced_shape), output_len, nims 



def test_sliced_output():
    im = f"{testdir}/exampledata/Line_clip451_flat_reg_nocosmics.fits"
    rotfile = f"{testdir}/exampledata/rotoff_noLinecosmics.fits"
    sliced_shape, output_len, nims = slicecube(im, rotfile)

    assert len(np.unique(sliced_shape)) == 1
    assert output_len == nims
    

if __name__ == "__main__":
    test_sliced_output()