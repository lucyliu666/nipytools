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
    return ndimage.measurements.center_of_mass(data)

def geometric_center(data):
    """
    Return the geometric center of the data.

    """
    coord = np.nonzero(data)
    max_coord = map(np.max, coord)
    min_coord = map(np.min, coord)
    return (np.array(max_coord) + np.array(min_coord))/2

def get_roi_coord(roi_data):
    """
    Get coordinates of a ROI.

    """
    coords = roi_data.nonzero()
    vxl_num = coords[0].shape[0]
    c = [[coords[0][i], coords[1][i], coords[2][i]] for i in range(vxl_num)]
    return c

def load_coord_file(coord_file):
    """
    Load a file containing coordinates.

    """
    info = open(coord_file).readlines()
    info = [line.strip().split(',') for line in info]
    c = []
    for line in info:
        temp = [int(item) for item in line]
        c.append(line)
    return c

def get_x_flipped_coord(coord):
    """
    Return the voxel coordinates flipped along x axis.

    """
    c = [[90 - line[0], line[1], line[2]] for line in coord]
    return c

def get_voxel_value(coord, data):
    """
    Get voxel data based on input coordiantes.

    """
    v = [data[tuple(c)] for c in coord]
    return np.array(v)

def get_roi_peak_coord(roi_data, value_data):
    """
    Get the peak of a ROI based on value_data.

    """
    roi_data[roi_data>0] = 1
    masked_data = roi_data * value_data
    c = np.unravel_index(masked_data.argmax(), masked_data.shape)
    return c

def cube_roi(data, x, y, z, radius, value):
    """
    Generate a cube roi which center in (x, y, z).

    """
    for n_x in range(x - radius, x + radius + 1):
        for n_y in range(y - radius, y + radius + 1):
            for n_z in range(z - radius, z + radius + 1):
                try:
                    data[n_x, n_y, n_z] = value
                except IndexError:
                    pass
    return data

def sphere_roi(data, x, y, z, radius, value):
    """
    generate a sphere roi which center in (x, y, z).

    """
    for n_x in range(x - radius, x + radius + 1):
        for n_y in range(y - radius, y + radius + 1):
            for n_z in range(z - radius, z + radius + 1):
                n_coord = np.array((n_x, n_y, n_z))
                coord = np.array((x, y, z))
                if np.linalg.norm(coord - n_coord) <= radius:
                    try:
                        data[n_x, n_y, n_z] = value
                    except IndexError:
                        pass
    return data

def extract_mean_ts(source, mask):
    """Extract mean time course in a mask from source image."""
    mask[mask > 0] = 1
    mask[mask < 0] = 0
    src_dim = len(source.shape)
    if src_dim > 3:
        mask_size = mask.sum()
        source_len = source.shape[3]
        mask = np.expand_dims(mask, axis=3)
        mask = np.repeat(mask, source_len, axis=3)
        mask = mask.reshape(-1, source_len)
        s = source.reshape(-1, source_len)
        s = s * mask
        data = s.sum(axis=0) / mask_size
    else:
        source = source * mask                                                  
        data = source.sum() / mask.sum()
        data = np.array([data])
    return data

