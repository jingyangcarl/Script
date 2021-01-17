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

file_transform_path = 'D:/Marcel/transforms_raw.txt'
sh_folder_path = 'D:/data/lightProbe/Original/png/spherical_harmonics'
sh_name = 'Chelsea_Stairs_3k'

index_test = [10, 14, 16]
index_val = [12, 18, 20]
output_path = 'D:/data/Marcel/rendered'
out_json = {
    'frames': []
}
out_json_test = {
    'frames': []
}
out_json_val = {
    'frames': []
}
out_json_train = {
    'frames': []
}

with open(file_transform_path) as file_transform:
    transforms_txt = file_transform.read().split('\n')

entry_len = 17
for index in range(round(len(transforms_txt) / entry_len)):
    name = transforms_txt[index]
    angle_of_view = 50. / 180. * np.pi
    res = [800, 800]
    focal = .5 * res[0] / np.tan(.5 * angle_of_view)
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
        'file_path': './unclassified/{}/rendered_{}'.format(sh_name, index+1),
        'hwf': hwf2list(res, focal),
        'transform_matrix': transform2list(transform),
        'sh': sh2list(sh_name)
    })
    if index+1 in index_test:
        out_json_test['frames'].append({
            'file_path': './unclassified/{}/rendered_{}'.format(sh_name, index+1),
            'hwf': hwf2list(res, focal),
            'transform_matrix': transform2list(transform),
            'sh': sh2list(sh_name)
        })
    elif index+1 in index_val:
        out_json_val['frames'].append({
            'file_path': './unclassified/{}/rendered_{}'.format(sh_name, index+1),
            'hwf': hwf2list(res, focal),
            'transform_matrix': transform2list(transform),
            'sh': sh2list(sh_name)
        })
    else:
        out_json_train['frames'].append({
            'file_path': './unclassified/{}/rendered_{}'.format(sh_name, index+1),
            'hwf': hwf2list(res, focal),
            'transform_matrix': transform2list(transform),
            'sh': sh2list(sh_name)
        })

# output to json
with open('{}/{}/transforms.json'.format(output_path, sh_name), 'w') as out_file:
    json.dump(out_json, out_file, indent=4)
with open('{}/{}/transforms_test.json'.format(output_path, sh_name), 'w') as out_file_test:
    json.dump(out_json_test, out_file_test, indent=4)
with open('{}/{}/transforms_val.json'.format(output_path, sh_name), 'w') as out_file_val:
    json.dump(out_json_val, out_file_val, indent=4)
with open('{}/{}/transforms_train.json'.format(output_path, sh_name), 'w') as out_file_train:
    json.dump(out_json_train, out_file_train, indent=4)
