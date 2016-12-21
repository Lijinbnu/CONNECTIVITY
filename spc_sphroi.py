import os
import numpy as np
import nibabel as nib
import pandas as pd
import csv 
import random
import re

"""
def get_roi_file(subj_dir):
    f_list = os.listdir(subj_dir)
    for f in f_list:
        if re.search('_ff.nii.gz', f):
            return os.path.join(subj_dir, f)
"""
def vox2MNI(vox,affine):
    vox_new = np.ones([4,1])
    vox_new[0:-1,0] = vox[:]
    MNI = affine.dot(vox_new)
    MNI_new = MNI[0:-1].tolist()
    return sum(MNI_new,[])


def sphere_roi(data, x, y, z, radius, value):
    for n_x in range(x - radius, x + radius + 1):
        for n_y in range(y - radius, y + radius + 1):
            for n_z in range(z - radius, z + radius+ 1):
                n_coord = np.array((n_x, n_y, n_z))
                coord = np.array((x, y, z)) 
                if np.linalg.norm(coord - n_coord) <= radius:
                    try:
                        data[n_x,n_y,n_z] = value
                    except IndexError:
                       pass
    return data

# input varible,sessid
obj_file = open('/nfs/h1/workingshop/lijin/CONNECTIVITY/subjID_190','rU')
sessid = obj_file.read().splitlines()
obj_file.close()

# output path
outpath_par = '/nfs/h1/workingshop/lijin/CONNECTIVITY/regionalwise_FC/'
sesspar = '/nfs/h1/workingshop/lijin/CONNECTIVITY/DATA/'
# lbname
areaname = ['r_OFA','l_OFA','r_pFus','l_pFus','rp_STS','lp_STS']
# lbid
areaid = [1,2,3,4,9,10]

# input variable,task
task = 'fa'
# input variable, contrast
contrast = 'face-object'
idnum = len(sessid)
#areanum = 6
#radius = 1


#mpsc = np.zeros([idnum,areanum])
#mzstat = np.zeros([idnum,areanum])
#peak_cor = np.zeros([idnum,areanum,3])
#peak_cor_MNI = np.zeros([idnum,areanum,3])
#sessi  = 0

output_file = r'spc_sph_roi.csv'
f = open(output_file, 'wb')
f.write('SID,label_idx,roi_size,x,y,z,sph_vox\n')

sphereroi = []

for sess in sessid:
    print sess
    pathroi = os.path.join(sesspar, sess,task,contrast,'core_roi.nii.gz')
    data_roi = nib.load(pathroi).get_data()
    
    #pathbeta = os.path.join(sesspar,sess,contrast,'cope1.nii.gz')
    pathstat = os.path.join(sesspar,sess,task,contrast,'zstat1_3mm.nii.gz')
    data_zsta = nib.load(pathstat).get_data()
    
    pathrest = os.path.join(sesspar,sess,'subj_mask_abs.nii.gz')
    roi_rest = nib.load(pathrest).get_data()

    affine = nib.load(pathstat).get_affine()
    #header = img_zsta.get_header()

    unique_label = np.unique(data_roi)

    sph_roi_all = np.zeros((60, 72, 60))
    for idx in areaid:
        if not idx:
            continue

        outstr = [sess, str(idx)]
        print '# %d' % (idx)
        tmp_mask = data_roi==idx
        roi_size = np.sum(tmp_mask)
        print roi_size # origin roi size
        outstr.append(str(roi_size))
        if roi_size == 0:
            continue
        tmp_zsta = tmp_mask * data_zsta
        coord = np.unravel_index(tmp_zsta.argmax(), tmp_zsta.shape)
        coord_MNI = vox2MNI(coord,affine)
        print coord_MNI
        for c in coord_MNI:
            outstr.append(str(c))
        roi_sphere = np.zeros((60, 72, 60))
        roi_sphere = sphere_roi(roi_sphere, int(coord[0]), int(coord[1]), int(coord[2]), 2, idx)
        n_sphere = np.count_nonzero(roi_sphere) # local max raw sph, eg. number = 33
        print n_sphere
        outstr.append(str(n_sphere))
        
        sphroi_mask = roi_sphere * roi_rest
        voxel =  np.count_nonzero(sphroi_mask)
        print voxel
        outstr.append(str(voxel))
        f.write(','.join(outstr)+'\n')

        sph_roi_all[sphroi_mask !=0] = idx

        #meanz = np.nanmean(data_zsta[roi_sph == idx])
        #outstr.append(str(meanz))
        #peak_z = np.nanmax(data_zsta[tmp_mask])
        #peak_z = data_zsta[tmp_mask].argmax()
        #outstr.append(str(peak_z))
        #outstr.append(str(n_voxel))
        #outstr.append(str(roi_size))
        f.write(','.join(outstr)+'\n')

    sphereroi = nib.Nifti1Image(sph_roi_all,affine)
    sph_name = sesspar + '/' + sess + '/' + task + '/' + contrast +'/'+ 'core_roi_sph_spc' + '.nii.gz'
    nib.save(sphereroi,sph_name)
    

"""
    sphereroi = nib.Nifti1Image(sph_roi,affine)
    sph_name = 'sphere'+ sess + '.nii.gz'
    nib.save(sphereroi,sph_name)
"""

"""
        temp = np.zeros([91,109,91])
        data = np.zeros([91,109,91])

        if data_beta[data_face == (areai+1)] != []: 
           #peak coordinate
           temp[data_face == (areai+1)] = data_zsta[data_face == (areai+1)]
           peak_cor[sessi,areai,:] = np.unravel_index(temp.argmax(),temp.shape)
           if not any(peak_cor[sessi,areai,:]):
               peak_cor[sessi,areai,:] = [np.nan,np.nan,np.nan]
           peak_cor_MNI[sessi,areai,:] = vox2MNI(peak_cor[sessi,areai,:],affine)
           px = peak_cor[sessi,areai,0]
           py = peak_cor[sessi,areai,1]
           pz = peak_cor[sessi,areai,2]
           print 'Area #: %d' %(areai+1)
           print '%d %d %d'%(px, py, pz)

           if px != []:
              roi_sphere = sphere_roi(data, int(px), int(py), int(pz), 1, 1)
                
               # img_face_sphere = nib.load(roi_sphere)
               # data_face_sphere = roi_sphere
  
               #pathbeta = os.path.join(sesspar,sess,contrast,'cope1.nii.gz')
               #pathstat = os.path.join(sesspar,sess,contrast,'zstat1.nii.gz')
               #img_zsta = nib.load(pathstat)
               #data_zsta = img_zsta.get_data()

               
              if data_beta[roi_sphere == (areai+1)] != []:
                 #mpsc[sessi,areai] = np.nanmean(data_beta[data_face == (areai+1)])
                 mzstat[sessi,areai] = np.nanmean(data_zsta[roi_sphere == 1])
    sessi+=1

outpath = os.path.join(outpath_par,'sphere_rawcsv')
for areai in range(areanum):
    with open(os.path.join(outpath,areaname[areai]+'.csv'),'wb') as filecsv:
         writer_total = csv.writer(filecsv)
         writer_total.writerow(['NSPID',
                                'mean_zstate_sphere',
                                'px','py','pz'])
         wholedata_total = zip(list(sessid),
                           list(mzstat[:,areai]),
                           list(peak_cor_MNI[:,areai,0]),
                           list(peak_cor_MNI[:,areai,1]),
                           list(peak_cor_MNI[:,areai,2]))
         writer_total.writerows(wholedata_total)
    filecsv.close()
#print peak_cor_img
"""
