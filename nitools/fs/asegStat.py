# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Get measurement of surface

"""
import os

src_dir = r'/nfs/t1/nsppara/corticalsurface'
cmd_name = '/usr/local/neurosoft/freesurfer/bin/mri_segstats'
sessid = open('sessid').readlines()
sessid = [line.strip() for line in sessid]

for subj in sessid:
    f = open(subj + '_aseg.sh', 'w')
    task_name = subj + 'seg_stats'
    seg_file = os.path.join(src_dir, subj, 'mri', 'aseg.mgz')
    pv_file = os.path.join(src_dir, subj, 'mri', 'norm.mgz')
    cmd_str = cmd_name + ' --seg ' + seg_file + ' --id 18 --id 54 ' + '--pv ' + pv_file + ' --sum ' + subj + '.sum --etiv --subject ' + subj + '\n'
    f.write('#! /bin/bash\n')
    f.write('#$ -N ' + task_name + '\n')
    f.write('#$ -S /bin/bash\n')
    f.write('#$ -V\n')
    f.write('#$ -cwd\n')
    f.write('#$ -q short.q\n')
    f.write(cmd_str)
    f.close()
    os.system('qsub ' + subj + '_aseg.sh')
