# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
import scipy.ndimage as ndimage
import skimage.morphology as skmorph

def distance_transformation(data):
    dist = ndimage.distance_transform_edt(data)
    return -dist

def gradient_transformation(data):
    gx = ndimage.sobel(data, 0)
    gy = ndimage.sobel(data, 1)
    gz = ndimage.sobel(data, 2)
    grad = np.sqrt(gx**2 + gy**2 + gz**2)
    return grad

def inverse_transformation(data):
    return -data

def merge_peak(data, marker, dthr):
    x, y, z = marker.nonzero()
    
    for i in range(x.shape[0]):
        if not marker[x[i], y[i], z[i]]:
            continue
        for j in range(i+1, x.shape[0]):
            if not marker[x[j], y[j], z[j]]:
                continue
            if (np.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2+(z[i]-z[j])**2)) <= dthr:
                if data[x[i], y[i], z[i]] >= data[x[j], y[j], z[j]]:
                    marker[x[j], y[j], z[j]] = 0
                else:
                    marker[x[i], y[i], z[i]] = 0
    return marker

def mass_center(data):
    """
    Return the center of mass of the data.

    """
    return ndimage.meansurements.center_of_mass(data)

def geometric_center(data):
    """
    Return the geometric center of the data.

    """
    coord = np.nonzero(data)
    max_coord = map(np.max, coord)
    min_coord = map(np.min, coord)
    return (np.array(max_coord) + np.array(min_coord))/2
