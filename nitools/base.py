# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import nibabel as nib
import subprocess

def vxl2mni(coordlist):
    """
    Return a list of coordinate in MNI space of FSL standard template (2mm)
    based on input coordinate list in ijk space.

    """
    mni_list = []
    for item in coordlist:
        temp = (90 - 2 * item[0],
                -126 + 2 * item[1],
                -72 + 2 * item[2])
        mni_list.append(temp)
    return mni_list

def mni2vxl(coord):
    """Return the coordinate in voxel/ijk space of FSL standard template (2mm)
    based on input MNI coordinate.
    """
    i = int((90.0 - coord[0]) / 2)
    j = int((coord[1] + 126) / 2)
    k = int((coord[2] + 72) / 2)
    return (i, j, k)

def read_par(par_file, tr):
    info = open(par_file).readlines()
    info = [line.strip().split() for line in info]
    par_info = dict()
    for line in info:
        if not line[4] in par_info:
            par_info[line[4]] = []
        start_t = int(float(line[0]) / tr)
        duration_t = int(float(line[2]) / tr)
        for t in range(start_t, start_t + duration_t):
            par_info[line[4]].append(t)
    return par_info

def run_save_cmd(cmd_list, f):
    f.write(' '.join(cmd_list) + '\n')
    subprocess.call(cmd_list)

def save2nifti(data, affine, file_name):
    """
    Save data to a nifti file.

    """
    img = nib.Nifti1Image(data, affine)
    nib.save(img, file_name)

