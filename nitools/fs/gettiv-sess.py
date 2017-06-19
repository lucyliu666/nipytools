# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Get TIV for each subject

"""
import os
import subprocess

sessid_file = r'/nfs/j3/userhome/huanglijie/sessid'
out_file = r'/nfs/j3/userhome/huanglijie/tiv.txt'

src_dir = r'/nfs/t1/nsppara/corticalsurface'
cmd_name = '/usr/local/neurosoft/freesurfer/bin/mri_segstats'

sessid = open(sessid_file).readlines()
sessid = [line.strip() for line in sessid]

f = open(out_file, 'wb')
f.write('SID, TIV\n')

for subj in sessid:
    out = subprocess.check_output(['mri_segstats', '--subject',
                                   subj, '--etiv-only'])
    out = out.split('\n')[8]
    out = out.split()[3]
    f.write(','.join([subj, out]) + '\n')

