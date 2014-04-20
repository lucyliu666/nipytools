# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import subprocess

subjects_dir = '/nfs/t1/nsppara/corticalsurface'
subjects_list = open('sessid').readlines()
subjects_list = [line.strip() for line in subjects_list]

src_file_name = ['posterior_left_CA1',
                 'posterior_left_CA2-3',
                 'posterior_left_CA4-DG',
                 'posterior_Left-Cerebral-Cortex',
                 'posterior_Left-Cerebral-White-Matter',
                 'posterior_left_fimbria',
                 'posterior_left_hippocampal_fissure',
                 'posterior_Left-Hippocampus',
                 'posterior_left_presubiculum',
                 'posterior_left_subiculum',
                 'posterior_right_CA1',
                 'posterior_right_CA2-3',
                 'posterior_right_CA4-DG',
                 'posterior_Right-Cerebral-Cortex',
                 'posterior_Right-Cerebral-White-Matter',
                 'posterior_right_fimbria',
                 'posterior_right_hippocampal_fissure',
                 'posterior_Right-Hippocampus',
                 'posterior_right_presubiculum',
                 'posterior_right_subiculum']

for subj in subjects_list:
    src_dir = os.path.join(subjects_dir, subj, 'mri')
    targ_dir = os.path.join(src_dir, 'hippocampus')
    subprocess.call(['mkdir', targ_dir])
    script_name = subj + '_convert.sh'
    f = open(script_name, 'w')
    f.write('#! /bin/bash\n')
    f.write('#$ -N convert_' + subj + '\n')
    f.write('#$ -S /bin/bash\n')
    f.write('#$ -V\n')
    f.write('#$ -cwd\n')
    f.write('#$ -q short.q\n')
    for src_file in src_file_name:
        src_f = os.path.join(src_dir, src_file + '.mgz')
        targ_f = os.path.join(targ_dir, src_file + '.nii.gz')
        targ_2mm_f = os.path.join(targ_dir, src_file + '_2mm.nii.gz')
        nu_f = os.path.join(src_dir, 'nu.mgz')
        f.write('/usr/local/neurosoft/freesurfer/bin/mri_convert ' + src_f + ' ' + targ_f + '\n')
        f.write('/usr/local/neurosoft/freesurfer/bin/mri_label2vol --seg ' + targ_f + ' --temp ' + nu_f + ' --regheader --o ' + targ_f + '\n')
        f.write('/usr/local/neurosoft/freesurfer/bin/mri_convert --out_orientation LAS ' + targ_f + ' ' + targ_f + '\n')
        f.write('/usr/local/neurosoft/freesurfer/bin/mri_convert -vs 2 2 2 ' + targ_f + ' ' + targ_2mm_f + '\n')
    f.close()
    os.system('qsub ' + script_name)
