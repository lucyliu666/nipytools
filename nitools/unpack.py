# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Module pyunpack provides basic functions for processing scanlist and 
is utilized to unpack dicom files.

Example:

    >>> import unpack
    >>> unpack? 

Edited By Lijie Huang, 2011-10-31
Last modified by Lijie Huang, 2012-9-3

"""

import os
import tarfile
import subprocess
import numpy as np
from session import Session


def readscanlist(scanlist_file):
    """
    Read scanlist file and store the information in several dictionaries.

    Usage:
         [scanInfo, subjList] = readScanlist(scanlistFile)
         scanlistFile --> absolute path of the scanlist file (csv file)

    Example:
    --------

    >>> scanlistFile = r'/nfs/s2/test/scanlist.csv'
    >>> [scanInfo, subjList] = readScanlist(scanlistFile)

    """
    if os.path.exists(scanlist_file):
        scan = {}
        subj_list = []
        scanlist = open(scanlist_file)
        lines = scanlist.readlines()
        lines = [line.rstrip('\r\n') for line in lines]

        # Get information from first 6 line of the header file
        for num in range(6):
            tmp = lines[num].split(',')
            scan[tmp[0]] = tmp[1].strip()

        # Get information of experiment name
        tmp = lines[6].split(',')
        exp_list = []
        for num in range(1,tmp.index('')):
            exp_list.append(tmp[num].strip())
        scan[tmp[0]] = exp_list

        # Get every session information
        exp_label = lines[7].split(',')
        for num in range(8,len(lines)):
            tmp = lines[num].split(',')
            if tmp[2] == '':
                break
            subj = Session(tmp[2], tmp[0])
            subj.dicom_ID = tmp[1]
            for run_index in range(3, len(tmp)):
                if tmp[run_index] != '':
                    if exp_label[run_index] in scan['expname']:
                        subj.setruninfo(exp_label[run_index],
                                        tmp[run_index],
                                        tmp[run_index + 1])
                    elif exp_label[run_index] == 'par':
                        pass
                    else:
                        subj.setruninfo(exp_label[run_index],
                                        tmp[run_index],
                                        '')
            subj_list.append(subj)
        return scan, subj_list
    else:
        print 'Scanlist file does not exist, please check it out.\n'

def untarsess(scanlist_file, src_dir='None'):
    """
    According to the scanlist, untar orig dicom data into dicomdir.
    Default tar.gz files and untared files are all in dicomdir.

    Usage:
        untarsess(scanlistFile, srcDir)
    Parameters:
        scanlistFile --> absolute path of scanlist file
        srcDir --> source directory containing the tar.gz file, default
                   is 'None'
 
    Example:
    --------

    >>> scanlistFile = r'/nfs/s2/test/scanlist.csv'
    >>> untarsess(scanlistFile)

    """
    [scan, subj_list] = readscanlist(scanlist_file)
    dicom_dir = scan['dicomdir']
    if src_dir == 'None':
        src_dir = scan['dicomdir']
    if not os.path.exists(dicom_dir):
        print 'Directory ' + dicom_dir + ' does not exist, create one \
               automatically.'
        subprocess.call(['mkdir', dicom_dir])
    untar_error_file = os.path.join(dicom_dir, 'untarError.log')
    untar_error_info = open(untar_error_file, 'a')
    for subj in subj_list:
        tar_file = subj.dicom_ID.upper() + '.tar.gz'
        src_file = os.path.join(src_dir, tar_file)
        srcdir_path = os.path.join(src_dir, subj.dicom_ID.upper())
        if not os.path.exists(src_file):
            if os.path.exists(srcdir_path):
                if not src_dir == dicom_dir:
                    subprocess.call(['cp', '-r', srcdir_path, dicom_dir])
                else:
                    untar_error_info.write('No change for directory ' + \
                                           srcdir_path + '\n')
            else:
                untar_error_info.write('File ' + src_file + \
                                       ' does not exist.\n')
        else:
            tar = tarfile.open(src_file)
            tar.extractall(path=dicom_dir)
    untar_error_info.close()

def unpacksdcm(src_dir, targ_dir, mode, scan_info_name='None', 
               cfg=[], error_file='none'):
    """
    src_dir and targ_dir must be the absolute address.

    Example:
    --------

    unpacksdcm('/nfs/s2/rawdata/S0001', '/nfs/s2/data/S0001', 'scanonly',
               scan_info_name='scan.info')

    Or:

    unpacksdcm('/nfs/s2/rawdata/S0001',
               '/nfs/s2/data/S0001',
               'unpack',
               cfg=[' -run 1 bold nii.gz f.nii.gz',
                    ' -run 2 bold nii.gz f.nii.gz'],
               error_file='error.log')

    """
    if mode == 'scanonly':
        if scan_info_name != 'None':
            scan_info_file = os.path.join(targ_dir,scan_info_name)
            cmdstr = 'unpacksdcmdir -src ' + src_dir + ' -targ ' + \
                     targ_dir + ' -scanonly ' + scan_info_file
            subprocess.call(cmdstr.split())
        else:
            print 'Please specify a scaninfo file name.\n'
    elif mode == 'unpack':
        if os.path.exists(src_dir):
            if len(cfg) != 0:
                cmdstr = 'unpacksdcmdir,-src,' + src_dir + ',-targ,' + \
                         targ_dir + ',-fsfast'
                for item in cfg:
                    cmdstr = cmdstr + item
                print cmdstr
                unpack_file = os.path.join(targ_dir, 'unpackcmd')
                unpacklog = open(unpack_file, 'a')
                unpacklog.write(cmdstr + '\n')
                unpacklog.close()
                subprocess.call(cmdstr.split(','))
            else:
                errorInfo = open(error_file, 'a')
                errorInfo.write('Error: cfg list contains nothing.\n')
                errorInfo.close()
        else:
            errorInfo = open(error_file, 'a')
            errorInfo.write('Source directory does not exist.\n')
            errorInfo.close()
    else:
        print 'You specified a wrong mode parameter.\n'
 
def scandcm(dicom_ID, sess_ID, src_dir, targ_dir, scaninfo_file):
    """
    Scan a subject's session information and put result in a scan_info file.

    Example:
    --------

    scandcm(dicomid, sessid, srcDir, targDir, 'scan.info')

        scrdir is directory with the DICOM files
        targdir is top directory into which the files will be unpacked

    """
    src_dir = os.path.join(src_dir, dicom_ID.upper())
    log_file = os.path.join(targ_dir, 'error.log')
    targ_dir = os.path.join(targ_dir, sess_ID)
    if not os.path.exists(src_dir):
        error_info = open(log_file, 'a')
        error_info.write('Source dir ' + src_dir + ' does not exist.\n')
        error_info.close()
    else:
        unpacksdcm(src_dir, targ_dir, 'scanonly', scan_info_name=scaninfo_file)
    
def scandcmsess(scanlist_file, scan_info_name='scan.info'):
    """
    According to the scanlist, scan every session's information and store 
    result in a scan.info file (stored in sessdir).

    Example:
    --------

    scandcmsess(scanlistFile, scanInfoName)

        Default scanInfoName is 'scan.info'

    """
    # Get scan information from scanlist file
    [scan, subj_list] = readscanlist(scanlist_file)
    src_dir = scan['dicomdir']
    targ_dir = scan['sessdir']
    if not os.path.exists(targ_dir):
        print 'Session dir ' + targ_dir + ' does not exist, create it \
              automatically.'
        subprocess.call(['mkdir', targ_dir])

    for subj in subj_list:
        scandcm(subj.dicom_ID, subj.sess_ID, src_dir, targ_dir, scan_info_name)

def checkrun(run_index, seq_name, scan_size, dicom_ID, scan_info_file):
    """
    Check one certain run's quility.

    Example:
    --------

    checkrun(runIndex, seqName, scanSize, dicom_ID, scanInfoFile)

    >>> checkSeq('9', 'localizer', [512 512 3 1], '20110404_10_S0001_XXX',
                 '/nfs/s2/data/S0001/scan.info')

        scanInfoFile is the address of scaninfo file.

    """
    if os.path.exists(scan_info_file):
        scan = open(scan_info_file)
        scan_info = scan.readlines()
        run_No = []
        run_type = []
        run_stat = []
        run_size = []
        session_ID = []
        for x in scan_info:
            tmp = x.split()
            run_No.append(tmp[0])
            run_type.append(tmp[1])
            run_stat.append(tmp[2])
            run_size.append([int(tmp[3]), int(tmp[4]), 
                             int(tmp[5]), int(tmp[6])])
            session_ID.append(tmp[7].split('.')[0])

        if run_index in run_No:
            num = run_No.index(run_index)
            if seq_name != run_type[num]:
                print 'run ' + run_index + "'s sequence name does not match.\n"
            else:
                if run_stat[num] != 'ok':
                    print 'run ' + run_index + ' has something wrong.\n'
                else:
                    if scan_size != run_size[num]:
                        print 'run ' + run_index + "'s size does not match. "
                        print 'Current size is ' + str(run_size[num]) + '.\n'
                    else:
                        if dicom_ID != session_ID[num]:
                            print 'run ' + run_index + "'s dicomID does not match."
                            print 'Current dicom ID is ' + session_ID + '.\n'
                        else:
                            print 'run ' + run_index + ' pass!\n'
        else:
            print 'run ' + run_index + ' does not exist.\n'
    else:
        print 'scaninfo file does not exist.\n'

def checksess(scanlist_file, exp_name, seq_name, 
              scan_size, scan_info_name='scan.info'): 
    """
    Check run qulity of certain texperiment for all subjects in scanlist.

    Example:
    --------

    >>> checksess(scanlistFile, expName, seqName, scanSize)

    """
    [scan, subj_list] = readscanlist(scanlist_file)
    targ_dir = scan['sessdir']

    for subj in subj_list:
        if exp_name in subj.run_info.keys():
            scan_info_file = os.path.join(targ_dir, subj.sess_ID, 
                                          scan_info_name)
            print '----------------------------------\n'
            print subj.sess_ID + ':\n'
            for run_index in subj.run_info[exp_name].keys():
                checkrun(run_index, seq_name, scan_size, 
                         subj.dicom_ID.upper(), scan_info_file)
        else:
            print exp_name + ' does not in ' + subj.sess_ID + "'s run list.\n"

def unpackscan(subj, exp_name, src_dir, targ_dir, sub_dir, format, name):
    """
    Unpack dicom file of a session

    Example:
    --------

    unpackscan(subj, taskName, srcDir, targDir, subDir, format, name)

    """
    src_dir = os.path.join(src_dir, subj.dicom_ID.upper())
    error_log = os.path.join(targ_dir, 'unpackError.log')
    error_info = open(error_log, 'a')
    error_info.write('--------------------------------\n')
    error_info.write(subj.sess_ID + ':\n')
    targ_dir = os.path.join(targ_dir, subj.sess_ID)
    exp_length = len(exp_name)
    cfg_info = []
    for index in range(exp_length):
        exp_item = exp_name[index]
        if exp_item in subj.run_info.keys():
            [run_index_list, par_file_list] = subj.getruninfo(exp_item)
            for run in run_index_list:
                cfg_info.append(','.join([',-run',
                                          run,
                                          sub_dir[index],
                                          format[index],
                                          name[index]]))
        else:
            error_info.write('task ' + exp_name[index] + 
                             ' dose not in run list.\n')
    error_info.close()
    unpacksdcm(src_dir, targ_dir, 'unpack',
               cfg=cfg_info, error_file=error_log)

def unpacksess(scanlist_file, exp_name, sub_dir, format, name):
    """
    Unpack dicom file

    Example:
    --------

    unpacksess('/nfs/s2/scanlist.csv',
               ['loc', 'mri'],
               ['loc', '3danat'],
               ['nii', 'nii'],
               ['f.nii.gz', '001.nii.gz'])

    """
    [scan, subj_list] = readscanlist(scanlist_file)
    src_dir = scan['dicomdir']
    targ_dir = scan['sessdir']

    if not os.path.exists(src_dir):
        print 'DicomDir ' + src_dir + ' does not exist.'
    elif not os.path.exists(targ_dir):
        print 'Session directory ' + targ_dir + ' does not exist, create it \
              automatically.'
        subprocess.call(['mkdir', targ_dir])
    else:
        for subj in subj_list:
            unpackscan(subj, exp_name, src_dir, targ_dir,
                       sub_dir, format, name)

def mkrlfsess(scanlist_file, exp_name, sub_dir):
    """
    Make run list file for certain task.

    Example:
    --------

    >>> mkrlfsess('/nfs/s2/scanlist.csv', 'mri', 'anat')

    """
    [scan, subj_list] = readscanlist(scanlist_file)
    src_dir = scan['dicomdir']
    targ_dir = scan['sessdir']
     
    for subj in subj_list:
        if exp_name in subj.run_info.keys():
            temp_subdir = os.path.join(targ_dir, subj.sess_ID, sub_dir)
            if not os.path.exists(temp_subdir):
                print 'Directory ' + temp_subdir + ' does not exist.'
            else:
                rlf_file = os.path.join(targ_dir, subj.sess_ID, 
                                        temp_subdir, 
                                        exp_name + '.rlf')
                rlf = open(rlf_file, 'w')
                strs = ''
                for run in subj.run_info[exp_name].keys():
                    strs = strs + run.zfill(3) + '\n'
                rlf.write(strs)
                rlf.close()
        else:
            print 'Experiment ' + exp_name + ' does not in run list \
                  of ' + subj.sess_ID + "'s.\n"

def copyparsess(scanlist_file, exp_name, sub_dir):
    """
    Copy par file for certain task.

    Example:
    --------

    >>> copyparsess('/nfs/s2/scanlist.csv', 'rh', 'bold1')

    """
    [scan, subj_list] = readscanlist(scanlist_file)
    src_dir = scan['dicomdir']
    targ_dir = scan['sessdir']
    par_dir = scan['pardir']

    for subj in subj_list:
        if exp_name in subj.run_info.keys():
            temp_targdir = os.path.join(targ_dir, subj.sess_ID, sub_dir)
            for run in subj.run_info[exp_name].keys():
                par_file = subj.run_info[exp_name][run]
                if par_file != '':
                    srcpar = os.path.join(par_dir, exp_name,
                                          exp_name + par_file + '.par')
                    tarpar = os.path.join(temp_targdir, run.zfill(3),
                                          exp_name + '.par')
                    subprocess.call(['cp', srcpar, tarpar])
        else:
            print 'Experiment ' + exp_name + ' does not in run list of ' + \
                  subj.sess_ID + "'s.\n"

def mksubjname(scanlist_file):
    """
    Make a subjectname file.

    Usage:
        mksubjname(scanlistFile)

    Example:
    --------

    >>> mksubjname('/nfs/s2/test/smp.csv')

    """
    [scan, subj_list] = readscanlist(scanlist_file)
    targ_dir = scan['sessdir']

    for subj in subj_list:
        sessid = subj.sess_ID
        subj_name_file = os.path.join(targ_dir, sessid, 'subjectname')
        subjname = open(subj_name_file, 'w')
        subjname.write(sessid + '\n')
        subjname.close()

def mksessid(scanlist_file, sessid_file_name='sessid'):
    """
    Make a sessid file based on scanlist file in your current working directory.

    Usage:
        mksessid(scanlist_file, sessid_file_name='sessid')

    Example:
    --------

    >>> mksessid('/nfs/s2/test/smp.csv')

    """
    [scan, subj_list] = readscanlist(scanlist_file)

    if os.path.exist(sessid_file_name):
        print 'File ' + sessid_file_name + ' exists, remove it automatically.\n'
        subprocess.call(['rm', sessid_file_name])
    sessid_file = open(sessid_file_name, 'a')
    for subj in subj_list:
        sessid_file.write(subj.sessID + '\n')

