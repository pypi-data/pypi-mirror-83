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


def slicecube(im, rotfile, datadir='./', slicedir='sliced/'):
    """
    This function slices a 3D cube of shape (N, y, x) where N is the number of frames into individual 2D images numbered sequentially

    Args:
        im (str): Name of the 3D image
        rotfile (str): Name of the cube containing the rotoff values needed to rotate images
        datadir (str): Directory containing the 3D image. Defaults to './'
        slicedir: Name of the directory to write the sliced images into. Defaults to 'sliced/'
    
    """

    # Read in 3D image, header, and rotoffs
    cube = fits.getdata(im)
    header = fits.getheader(im)
    rotoffs = fits.getdata(rotfile)

    # Record image dimensions
    nims, ydim, xdim = cube.shape

    # Check that rotoff and N dimension are same length
    if nims != len(rotoffs):
        raise IndexError('Number of images and number of rotoffs are not equal')

    # Create sliced directory if doesn't already exist
    if not os.path.exists(datadir+slicedir):
        os.makedirs(datadir+slicedir)

    # Save 2D images into the sliced directory
    for i in range(nims):
        sliced_im = cube[i,:,:]
        header["rotoff"]=rotoffs[i]
        fits.writeto(f"{datadir}{slicedir}sliced_{i+1}.fits", sliced_im, header, overwrite=True)

    print(f"Done creating individual images for KLIP. These live in the {datadir}{slicedir} directory")

