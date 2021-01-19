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
import shutil

def hwf2list(res, focal):
    return [res[0], res[1], focal]

def transform2list(transform):
    transform_list = []
    for row in np.asarray(transform.T):
        transform_list.append(row.tolist())
    return transform_list

def sh2list(sh_name):
    with open('{}/original_sh/{}.txt'.format(input_sh_path, sh_name)) as sh_file:
        sh_txt = sh_file.read().strip()
        sh = np.matrix(sh_txt.replace('\n', ';'))
        sh_list = []
        for row in np.asarray(sh)[:16]:
            sh_list.append(row.tolist())
        return sh_list

input_xform_file = 'D:/data/Marcel/maya_xform_raw.txt' # from maya
input_rendered_path = 'D:/data/Marcel/rendered_800'
input_sh_path = 'D:/data/lightProbe/Original/png/spherical_harmonics'
input_lightProbe_path = 'D:/data/lightProbe/Original/exr'

output_path = 'D:/data/Marcel/model_1_partial'
output_light_path = os.path.join(output_path, 'light')
output_train_path = os.path.join(output_path, 'train')
output_test_path = os.path.join(output_path, 'test')
output_val_path = os.path.join(output_path, 'val')

angle_of_view = 50. / 180. * np.pi
res = [800, 800]

out_json = {
    'train': {'frames': []},
    'test': {'frames': []},
    'val': {'frames': []},
}
index_test = [10, 14, 16]
index_val = [12, 18, 20]

try:
    os.makedirs(output_light_path, exist_ok=True)
    os.makedirs(output_train_path, exist_ok=True)
    os.makedirs(output_test_path, exist_ok=True)
    os.makedirs(output_val_path, exist_ok=True)
except FileExistsError:
    print('directories already exist')
    pass

with open(input_xform_file) as file_xform:
    xform_txt = file_xform.read().split('\n')

light_paths = [f.path for f in os.scandir(input_rendered_path) if f.is_dir()]
for light_path in light_paths[:10]:
    light_name = os.path.basename(light_path)
    print(light_name)

    maya_xform_len = 17
    length = maya_xform_len
    for index in range(round(len(xform_txt) / length)):
        cam_name = xform_txt[index]
        cam_index = index+1
        focal = .5 * res[0] / np.tan(.5 * angle_of_view)
        transform = np.matrix('{} {} {} {}; {} {} {} {}; {} {} {} {}; {} {} {} {}'.format(
            xform_txt[index*length+1], xform_txt[index*length+2], xform_txt[index*length+3], xform_txt[index*length+4], 
            xform_txt[index*length+5], xform_txt[index*length+6], xform_txt[index*length+7], xform_txt[index*length+8], 
            xform_txt[index*length+9], xform_txt[index*length+10], xform_txt[index*length+11], xform_txt[index*length+12], 
            xform_txt[index*length+13], xform_txt[index*length+14], xform_txt[index*length+15], xform_txt[index*length+16]))

        dst_class = ''
        dst_path = ''
        if cam_index in index_test:
            dst_class = 'test'
            dst_path = output_test_path
        elif cam_index in index_val:
            dst_class = 'val'
            dst_path = output_val_path
        else:
            dst_class = 'train'
            dst_path = output_train_path

        out_json[dst_class]['frames'].append({
            'file_path': './{}/{}/rendered_{}'.format(dst_class, light_name, cam_index),
            'lightProbe_path': './light/{}'.format(light_name),
            'hwf': hwf2list(res, focal),
            'transform_matrix': transform2list(transform),
            'sh': sh2list(light_name)
        })

        png_src_path = os.path.join(input_rendered_path, light_name, 'rendered_{}.png'.format(cam_index))
        png_dst_path = os.path.join(dst_path, light_name, 'rendered_{}.png'.format(cam_index))
        os.makedirs(os.path.join(dst_path, light_name), exist_ok=True)
        shutil.copy2(png_src_path, png_dst_path)
        print(png_src_path)
        light_src_path = os.path.join(input_lightProbe_path, '{}.exr'.format(light_name))
        light_dst_path = os.path.join(output_light_path, '{}.exr'.format(light_name))
        shutil.copy2(light_src_path, light_dst_path)
        

with open('{}/transforms_train.json'.format(output_path), 'w') as out_file_train:
    json.dump(out_json['train'], out_file_train, indent=4)
with open('{}/transforms_test.json'.format(output_path), 'w') as out_file_test:
    json.dump(out_json['test'], out_file_test, indent=4)
with open('{}/transforms_val.json'.format(output_path), 'w') as out_file_val:
    json.dump(out_json['val'], out_file_val, indent=4)


# out_json = {
#     'frames': []
# }
# out_json_test = {
#     'frames': []
# }
# out_json_val = {
#     'frames': []
# }
# out_json_train = {
#     'frames': []
# }

# with open(file_transform_path) as file_transform:
#     transforms_txt = file_transform.read().split('\n')

# entry_len = 17
# for index in range(round(len(transforms_txt) / entry_len)):
#     name = transforms_txt[index]
#     angle_of_view = 50. / 180. * np.pi
#     res = [800, 800]
#     focal = .5 * res[0] / np.tan(.5 * angle_of_view)
#     transform = np.matrix('{} {} {} {}; {} {} {} {}; {} {} {} {}; {} {} {} {}'.format(
#         transforms_txt[index*entry_len+1], transforms_txt[index*entry_len+2], transforms_txt[index*entry_len+3], transforms_txt[index*entry_len+4], 
#         transforms_txt[index*entry_len+5], transforms_txt[index*entry_len+6], transforms_txt[index*entry_len+7], transforms_txt[index*entry_len+8], 
#         transforms_txt[index*entry_len+9], transforms_txt[index*entry_len+10], transforms_txt[index*entry_len+11], transforms_txt[index*entry_len+12], 
#         transforms_txt[index*entry_len+13], transforms_txt[index*entry_len+14], transforms_txt[index*entry_len+15], transforms_txt[index*entry_len+16]))

#     def hwf2list(res, focal):
#         return [res[0], res[1], focal]

#     def transform2list(transform):
#         transform_list = []
#         for row in np.asarray(transform.T):
#             transform_list.append(row.tolist())
#         return transform_list

#     def sh2list(sh_name):
#         with open('{}/original_sh/{}.txt'.format(sh_folder_path, sh_name)) as sh_file:
#             sh_txt = sh_file.read().strip()
#             sh = np.matrix(sh_txt.replace('\n', ';'))
#             sh_list = []
#             for row in np.asarray(sh)[:16]:
#                 sh_list.append(row.tolist())
#             return sh_list

#     out_json['frames'].append({
#         'file_path': './unclassified/{}/rendered_{}'.format(sh_name, index+1),
#         'hwf': hwf2list(res, focal),
#         'transform_matrix': transform2list(transform),
#         'sh': sh2list(sh_name)
#     })
#     if index+1 in index_test:
#         out_json_test['frames'].append({
#             'file_path': './test/{}/rendered_{}'.format(sh_name, index+1),
#             'hwf': hwf2list(res, focal),
#             'transform_matrix': transform2list(transform),
#             'sh': sh2list(sh_name)
#         })
#     elif index+1 in index_val:
#         out_json_val['frames'].append({
#             'file_path': './val/{}/rendered_{}'.format(sh_name, index+1),
#             'hwf': hwf2list(res, focal),
#             'transform_matrix': transform2list(transform),
#             'sh': sh2list(sh_name)
#         })
#     else:
#         out_json_train['frames'].append({
#             'file_path': './train/{}/rendered_{}'.format(sh_name, index+1),
#             'hwf': hwf2list(res, focal),
#             'transform_matrix': transform2list(transform),
#             'sh': sh2list(sh_name)
#         })

# # output to json
# with open('{}/{}/transforms.json'.format(output_path, sh_name), 'w') as out_file:
#     json.dump(out_json, out_file, indent=4)
# with open('{}/{}/transforms_test.json'.format(output_path, sh_name), 'w') as out_file_test:
#     json.dump(out_json_test, out_file_test, indent=4)
# with open('{}/{}/transforms_val.json'.format(output_path, sh_name), 'w') as out_file_val:
#     json.dump(out_json_val, out_file_val, indent=4)
# with open('{}/{}/transforms_train.json'.format(output_path, sh_name), 'w') as out_file_train:
#     json.dump(out_json_train, out_file_train, indent=4)
