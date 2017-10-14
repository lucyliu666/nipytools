# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import shutil
import subprocess
from pynit.base import unpack as pyunpack
from nitools.fsl.base import par2ev

def copypar(scanlist_file):
    """Copy par file for each separate calculation."""
    # get data info from scanlist file
    [scan_info, subj_list] = pyunpack.readscanlist(scanlist_file)

    # dir config
    par_dir = os.path.join(scan_info['pardir'], 'emo')
    nii_dir = scan_info['sessdir']

    for subj in subj_list:
        # get run infor for emo task
        sid = subj.sess_ID
        subj_dir = os.path.join(nii_dir, sid, 'emo')
        # get par index for each emo run
        if not 'emo' in subj.run_info:
            continue
        [run_idx, par_idx] = subj.getruninfo('emo')
        for i in range(len(run_idx)):
            run_dir = os.path.join(subj_dir, '00'+run_idx[i])
            lss_dir = os.path.join(run_dir, 'lss')
            os.system('mkdir '+lss_dir)
            pair_file = os.path.join(par_dir, 'pair_run_'+par_idx[i]+'.txt')
            os.system('cp %s %s'%(pair_file, lss_dir))
            for j in range(80):
                t_dir = os.path.join(lss_dir, 't%s'%(j+1))
                os.system('mkdir %s'%(t_dir))
                par_file = os.path.join(par_dir, 'run_%s_%s.par'%(par_idx[i], j+1))
                os.system('cp %s %s'%(par_file,os.path.join(t_dir,'trial.par')))
                par2ev(os.path.join(t_dir, 'trial.par'))            

def runfeat(scanlist_file):
    [scan_info, subj_list] = pyunpack.readscanlist(scanlist_file)

    # dir config
    doc_dir=os.path.abspath(os.path.join(scan_info['pardir'],'../doc/feat_emo'))
    nii_dir = scan_info['sessdir']
    
    # template config
    template_fsf = os.path.join(doc_dir, 'trial.fsf')

    for subj in subj_list:
        # get run infor for emo task
        sid = subj.sess_ID
        subj_dir = os.path.join(nii_dir, sid, 'emo')
        # get par index for each emo run
        if not 'emo' in subj.run_info:
            continue
        [run_idx, par_idx] = subj.getruninfo('emo')
        for i in range(len(run_idx)):
            run_dir = os.path.join(subj_dir, '00'+run_idx[i])
            lss_dir = os.path.join(run_dir, 'lss')
            for j in range(80):
                t_fsf = os.path.join(lss_dir, 't%s'%(j+1), 'design.fsf')
                with open(template_fsf, 'r') as fin:
                    with open(t_fsf, 'w') as fout:
                        for line in fin:
                            line = line.replace('SSS', sid)
                            line = line.replace('RRR', '00'+run_idx[i])
                            line = line.replace('TTT', 't%s'%(j+1))
                            fout.write(line)
                os.system('feat %s'%t_fsf)

def clcfeat(scanlist_file):
    [scan_info, subj_list] = pyunpack.readscanlist(scanlist_file)

    # dir config
    doc_dir=os.path.abspath(os.path.join(scan_info['pardir'],'../doc/feat_emo'))
    nii_dir = scan_info['sessdir']
    
    # template config
    template_fsf = os.path.join(doc_dir, 'trial.fsf')

    for subj in subj_list:
        # get run infor for emo task
        sid = subj.sess_ID
        subj_dir = os.path.join(nii_dir, sid, 'emo')
        # get par index for each emo run
        if not 'emo' in subj.run_info:
            continue
        [run_idx, par_idx] = subj.getruninfo('emo')
        for i in range(len(run_idx)):
            run_dir = os.path.join(subj_dir, '00'+run_idx[i])
            lss_dir = os.path.join(run_dir, 'lss')
            for j in range(80):
                t_fsf = os.path.join(lss_dir, 't%s'%(j+1), 'design.fsf')
                feat_dir = os.path.join(lss_dir, 't%s'%(j+1), 'func.feat')
                if os.path.exists(t_fsf):
                    os.system('rm %s'%t_fsf)
                else:
                    print 'No fsf file found - %s'%(t_fsf)
                if os.path.exists(feat_dir):
                    os.system('rm -rf %s'%feat_dir)
                else:
                    print 'No feat dir found - %s'%(feat_dir)

def standardizecope(scanlist_file, stage):
    """For stage 1: update feat reg;
    For stage 2: Apply nonlinear warp for cope files.
    """
    [scan_info, subj_list] = pyunpack.readscanlist(scanlist_file)
    # dir config
    nii_dir = scan_info['sessdir']
    imgs = ['cope', 'tstat', 'zstst', 'varcope']

    # warp source for nonlinear registration
    srcfiles = ['highres2standard_2mm.mat', 'highres2standard_warp_2mm.nii.gz']
    fsl_dir = os.getenv('FSL_DIR')
    mnistd = os.path.join(fsl_dir, 'data', 'standard',
                          'MNI152_T1_2mm_brain.nii.gz')

    for subj in subj_list:
        # get run infor for emo task
        sid = subj.sess_ID
        anat_dir = os.path.join(nii_dir, sid, '3danat', 'reg_fsl')
        emo_dir = os.path.join(nii_dir, sid, 'emo')
        # get par index for each emo run
        if not 'emo' in subj.run_info:
            continue
        [run_idx, par_idx] = subj.getruninfo('emo')
        for i in range(len(run_idx)):
            run_dir = os.path.join(emo_dir, '00'+run_idx[i])
            lss_dir = os.path.join(run_dir, 'lss')
            for j in range(80):
                feat_dir = os.path.join(lss_dir, 't%s'%(j+1), 'func.feat')
                print feat_dir
                funcreg = os.path.join(feat_dir, 'reg')
                if stage==1:
                    shutil.copy(mnistd, os.path.join(funcreg,'standard.nii.gz'))
                    for f in srcfiles:
                        shutil.copy(os.path.join(anat_dir, f),
                                    os.path.join(funcreg, f.replace('_2mm','')))
                    subprocess.call('fsl_sub -q veryshort.q updatefeatreg %s'%(feat_dir), shell=True)

def pemerge(scanlist_file):
    [scan_info, subj_list] = pyunpack.readscanlist(scanlist_file)

    # dir config
    doc_dir=os.path.abspath(os.path.join(scan_info['pardir'],'../doc/feat_emo'))
    nii_dir = scan_info['sessdir']
    
    # template config
    template_fsf = os.path.join(doc_dir, 'trial.fsf')

    for subj in subj_list:
        # get run infor for emo task
        sid = subj.sess_ID
        subj_dir = os.path.join(nii_dir, sid, 'emo')
        # get par index for each emo run
        if not 'emo' in subj.run_info:
            continue
        [run_idx, par_idx] = subj.getruninfo('emo')
        for i in range(len(run_idx)):
            run_dir = os.path.join(subj_dir, '00'+run_idx[i])
            lss_dir = os.path.join(run_dir, 'lss')
            for j in range(80):
                t_fsf = os.path.join(lss_dir, 't%s'%(j+1), 'design.fsf')
                feat_dir = os.path.join(lss_dir, 't%s'%(j+1), 'func.feat')
                if os.path.exists(t_fsf):
                    os.system('rm %s'%t_fsf)
                else:
                    print 'No fsf file found - %s'%(t_fsf)
                if os.path.exists(feat_dir):
                    os.system('rm -rf %s'%feat_dir)
                else:
                    print 'No feat dir found - %s'%(feat_dir)


if __name__ == '__main__':
    scanlist_file = r'/nfs/cell_b/project/emotionPro/doc/scanlist.csv'
    #copypar(scanlist_file)
    #runfeat(scanlist_file)
    #clcfeat(scanlist_file)
    #pemerge(scanlist_file)
    standardizecope(scanlist_file, 1)

