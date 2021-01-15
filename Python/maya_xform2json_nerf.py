# xform2matrix_maya
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is
###########################
# Input Data Hierarchy:
# ./calibration_raw.txt
# camera1
# 0.975149
# 0
# 0.221548
# 0
# 0.15829
# 0.699663
# -0.696718
# 0
# -0.155009
# 0.714473
# 0.682276
# 0
# -10.019561 tx
# 42.509909  ty
# 45.256711  tz
# 1
# camera2
# 0.991216
# ...
# PS: the transforms_raw.txt is generated from Script/Maya/get_xform.mel
###########################
# Output Data Hierarchy:
# ./transforms.json

###########################
import os
import numpy as np
import json


sh_folder_path = 'D:/data/lightProbe/Original/png/spherical_harmonics'
file_transform_path = 'D:/Marcel/transforms_raw.txt'
output_path = 'D:/Marcel'

out_json = {
    'frames': []
}

with open(file_transform_path) as file_transform:
    transforms_txt = file_transform.read().split('\n')

entry_len = 17
for index in range(round(len(transforms_txt) / entry_len)):
    name = transforms_txt[index]
    focal = 2620.5209560074
    res = [800, 800]
    transform = np.matrix('{} {} {} {}; {} {} {} {}; {} {} {} {}; {} {} {} {}'.format(
        transforms_txt[index*entry_len+1], transforms_txt[index*entry_len+2], transforms_txt[index*entry_len+3], transforms_txt[index*entry_len+4], 
        transforms_txt[index*entry_len+5], transforms_txt[index*entry_len+6], transforms_txt[index*entry_len+7], transforms_txt[index*entry_len+8], 
        transforms_txt[index*entry_len+9], transforms_txt[index*entry_len+10], transforms_txt[index*entry_len+11], transforms_txt[index*entry_len+12], 
        transforms_txt[index*entry_len+13], transforms_txt[index*entry_len+14], transforms_txt[index*entry_len+15], transforms_txt[index*entry_len+16]))

    def hwf2list(res, focal):
        return [res[0], res[1], focal]

    def transform2list(transform):
        transform_list = []
        for row in np.asarray(transform.T):
            transform_list.append(row.tolist())
        return transform_list

    def sh2list(sh_name):
        with open('{}/original_sh/{}.txt'.format(sh_folder_path, sh_name)) as sh_file:
            sh_txt = sh_file.read().strip()
            sh = np.matrix(sh_txt.replace('\n', ';'))
            sh_list = []
            for row in np.asarray(sh)[:16]:
                sh_list.append(row.tolist())
            return sh_list

    out_json['frames'].append({
        'file_path': './unclassified/rendered_{}'.format(index),
        'hwf': hwf2list(res, focal),
        'transform_matrix': transform2list(transform),
        'sh': sh2list('Bunker_04_Ref')
    })

# output to json
with open('{}/transforms.json'.format(output_path), 'w') as out_file:
    json.dump(out_json, out_file, indent=4)