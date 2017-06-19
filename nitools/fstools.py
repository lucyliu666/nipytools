# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os

def get_aseg_vol(aseg_stats_file, stru_name):
    """
    Get volume of segmented structure from aseg.stats file derived from
    FreSurfer pipelines.

    """
    aseg_info = open(aseg_stats_file).readlines()
    aseg_info = [line.strip() for line in aseg_info]
    for idx in range(13, 23):
        tmp_info = aseg_info[idx].split(',')
        tmp_info = [line.strip() for line in tmp_info]
        if tmp_info[1] == stru_name:
            return tmp_info[-2]
    for idx in range(68, 113):
        tmp_info = aseg_info[idx].split()
        if tmp_info[1] == stru_name:
            return tmp_info[-2]
    print 'Does not find the structure %s'%(stru_name)

