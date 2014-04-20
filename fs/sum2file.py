# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Get measurement of surface

"""
import os

sessid = open('sessid.csv').readlines()
sessid = [line.strip() for line in sessid]

f = open('out.csv', 'w')
f.write(','.join(['SID', 'ICV', 'L_Amy', 'R_Amy']) + '\n')

for subj in sessid:
    info = open(subj + '.sum').readlines()
    info = [line.strip() for line in info]
    temp_0 = info[13].split(',')[3]
    temp_1 = info[35].split()[3]
    temp_2 = info[36].split()[3]
    f.write(','.join([subj, temp_0, temp_1, temp_2]) + '\n')
