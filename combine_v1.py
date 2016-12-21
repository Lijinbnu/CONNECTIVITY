import nibabel as nib
import os 
import numpy as np


# input varible,sessid
obj_file = open('/nfs/h1/workingshop/lijin/CONNECTIVITY/subjID_190','rU')
sessid = obj_file.read().splitlines()
obj_file.close()

# output path
outpath_par = '/nfs/h1/workingshop/lijin/CONNECTIVITY/regionalwise_FC/'
sesspar = '/nfs/h1/workingshop/lijin/CONNECTIVITY/DATA/'
# lbname
#areaname = ['r_OFA','l_OFA','r_pFus','l_pFus','rp_STS','lp_STS']
# roi label which need to combine
areaid = [7,8,9,10]

# input variable,task
task = 'fa'
# input variable, contrast
contrast = 'face-object'
idnum = len(sessid)
#areanum = 6
#radius = 1

"""
#mpsc = np.zeros([idnum,areanum])
#mzstat = np.zeros([idnum,areanum])
#peak_cor = np.zeros([idnum,areanum,3])
#peak_cor_MNI = np.zeros([idnum,areanum,3])
#sessi  = 0

output_file = r'spc_roi_info.csv'
f = open(output_file, 'wb')
f.write('SID,label_idx,x,y,z,meanz,n_vox,roi_size\n')

sphereroi = []
"""

for sess in sessid:
    print sess
    pathroi = os.path.join(sesspar, sess,task,contrast,'face_z2.3_ff_3mm.nii.gz')
    data_roi = nib.load(pathroi).get_data()
    
    grp_mask = nib.load('/nfs/h1/workingshop/lijin/CONNECTIVITY/coreFN_groupmask_gm.nii.gz')
    grp_mask_data = grp_mask.get_data()


    #pathbeta = os.path.join(sesspar,sess,contrast,'cope1.nii.gz')
    pathstat = os.path.join(sesspar,sess,task,contrast,'zstat1_3mm.nii.gz')
    data_zsta = nib.load(pathstat).get_data()


    affine = nib.load(pathstat).get_affine()
    #header = img_zsta.get_header()

    tmp = np.zeros((60, 72, 60))
    tmp[data_roi ==1] =1
    tmp[data_roi ==2] =2
    tmp[data_roi ==3] =3
    tmp[data_roi ==4] =4

    #tmp_r = np.zeros((60, 72, 60))
    tmp[data_roi == 7] = 9
    tmp[data_roi == 9] = 9

    #tmp_l = np.zeros((60, 72, 60))
    tmp[data_roi == 8] = 10
    tmp[data_roi == 10] = 10

    core_roi = nib.Nifti1Image(tmp,affine)
    sph_name = sesspar + '/' + sess + '/' + task + '/' + contrast +'/'+ 'core_roi' + '.nii.gz'
    nib.save(core_roi,sph_name)

"""
    tmp = nib.Nifti1Image(img_tmp,affine)
    tmp_name = 'tmp.nii.gz'
    nib.save(tmp,tmp_name)
"""

