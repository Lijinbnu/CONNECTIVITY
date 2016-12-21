#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import re
import sys
import logging
import argparse
import csv
import numpy as np
import nibabel as nib
#import subprocess

sesspar = '/nfs/h1/workingshop/lijin/CONNECTIVITY/DATA/'
# input variable,task
task = 'fa'
# input variable, contrast
contrast = 'face-object'

fsessid = '/nfs/h1/workingshop/lijin/CONNECTIVITY/subjID_tmp'
fsessid = open(fsessid)
#    if fsessid:
#        fsessid = open(fsessid)
subject_list  = [line.strip() for line in fsessid]
#subject_list  = 'S0001'
#    else:
#        subject_list = [args.sess]

output_file = r'spc_rOFA_lOFA.csv'
f = open(output_file, 'wb')
f.write('SID,r\n')
#subj = 'S0001'
for subj in subject_list:
    pathroi = os.path.join(sesspar, subj,task,contrast,'core_roi_sph_spc.nii.gz')
    data_roi = nib.load(pathroi).get_data()
    unique_label = np.unique(data_roi)
    unique_label = unique_label[1:len(unique_label)]
    print unique_label
    c1 =  np.where(unique_label == 1)
    c2 =  np.where(unique_label == 2)
    #print c1,c2
    non = (np.array([], dtype = np.int64),)
    if cmp(tuple(c1[0]),tuple(non[0])) == 0 or cmp(tuple(c2[0]),tuple(non[0])) == 0:
    #if str(c1) == str(non) or str(c2) == str(non): #same function as the code above
        continue
    #print subj
    outstr = [subj]
    seed_ts_dir = os.path.join('/nfs/h1/workingshop/lijin/CONNECTIVITY/regionalwise_FC',subj,'seed_ts_spcsph')
    tc_file = os.path.join(seed_ts_dir,'core_roi_sph_spc_spcsph.txt')

    tcf = open(tc_file)
    tcf_list = []

    for line in tcf.readlines():
        l = [value for value in line.split()]
        tcf_list.append(l)
    tcf.close()

    mask = np.zeros((236, 1, 1))
    mask[:,0,0] = 1
    tcf_array = np.array(tcf_list)

    roi0_tc = tcf_array[:,c1]
    roi1_tc = tcf_array[:,c2]
    roi0_tc = roi0_tc[mask ==1]
    roi1_tc = roi1_tc[mask ==1]
        
    print roi0_tc[0],roi1_tc[0]


    roi_tc = np.array([roi0_tc, roi1_tc],dtype = 'float_')
    corr = np.corrcoef(roi_tc)
    r = corr[0,1]

    outstr.append(str(r))
    f.write(','.join(outstr) +'\n')

