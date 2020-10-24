# calibration_lookup2JSON_nerf
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is used to look up camera calibrations from a set of rendered images by its name and OUTPUT to a JSON file with nerf format, 
# where the name follows the following format
# Environ_{A}_model_{B}_cameraview_{C}_cameraDis_{D}_{E}_{F} from yajie
###########################
# Input Data Hierarchy:
# ./images
# ├── Envrion_10_model_0_camview_00170_cameraDis_13_00001_0.jpg
# ├── Envrion_10_model_0_camview_00309_cameraDis_10_00005_0.jpg
# ...
# ------------------------#
# ./camera
# ├── 01
# │   ├── camview_00001_distance_01.txt
# │   ├── camview_00001_distance_02.txt
# │   ...
# ├── 02
# ...
# ------------------------#
# ./camview_00001_distance_01.txt
# │ #focal length
# │ 1425.928935 1425.928935
# │ #principal point
# │ 1741 2609
# │ #resolution
# │ 3482 5218
# │ #distortion coeffs
# │ 2.446990 -21.708500 0.000000
# │ #camera tranformation matrix 1
# │ Rotation Euler X Y Z (degrees): 0.000000 0.000000 0.000000
# │ Translation : 3.119050 1.043762 16.834641
# │ MATRIX :
# │ 0.982997 -0.017065 0.182828 3.119050
# │ 0.018531 0.999808 -0.006315 1.043762
# │ -0.182685 0.009596 0.983125 16.834641
# │ 0.000000 0.000000 0.000000 1.000000
# ------------------------#
# ./spherical_harmonics
# ├── environment_in_order.txt # a list of spherical harmonics that can be found in ./original_sh
# └── original_sh
#     ├── 03-Ueno-Shrine_3k.txt
#     ├── 10-Shiodome_Stairs_3k.txt
#     ...
# ------------------------#
###########################
# # Output File
# {
#     "frames": [
#         {
#             "file_path": "path_to_frame",
#             "transform_matrix": [
#                 [
#                     -0.7377411127090454,
#                     -0.13523635268211365,
#                     0.6613994240760803,
#                     2.6661863327026367
#                 ],
#                 [
#                     0.6750837564468384,
#                     -0.14778819680213928,
#                     0.7227866649627686,
#                     2.9136462211608887
#                 ],
#                 [
#                     -7.450580596923828e-09,
#                     0.9797293543815613,
#                     0.20032529532909393,
#                     0.8075370788574219
#                 ],
#                 [
#                     0.0,
#                     0.0,
#                     0.0,
#                     1.0
#                 ]
#             ]
#         },
#         {
#             ...
#         }
#     ]
# }

import os
import numpy as np
import json

img_folder_path = '/home/ICT2000/jyang/Documents/Data/ForJing/renderedPhotos'
cam_folder_path = '/home/ICT2000/jyang/Documents/Data/ForJing/arbitraryCameras_30_adjust'
sh_folder_path = '/home/ICT2000/jyang/Documents/Data/ForJing/spherical_harmonics'
output_path = '/home/ICT2000/jyang/Documents/Data/ForJing'

out_json = {
    'frames': []
}

with open('{}/environment_in_order.txt'.format(sh_folder_path)) as sh_order_file:
    sh_order = sh_order_file.read().split('\n')

# walk through all images in img_path
for r, d, f in os.walk(img_folder_path):
    for file in f:
        if '.jpg' in file:
            # get file name
            # e.g.: Envrion_10_model_0_camview_00170_cameraDis_13_00001_0
            img_name = os.path.splitext(file)[0]

            # split file name with _
            args = img_name.split('_')

            # decompose parameters
            environ = int(args[1])
            model = int(args[3])
            cam_view = int(args[5])
            cam_dis = int(args[7])
            cam_dis_micro = int(args[8])

            # get relative cam path
            # e.g.: camview_00001_distance_01
            cam_name = 'camview_{:05d}_distance_{:02d}'.format(cam_view, cam_dis_micro)
            cam_path = '{}/{:02d}/{}.txt'.format(cam_folder_path, cam_dis, cam_name)

            # open cam calibration
            with open(cam_path) as cam_file:
                cam_args = cam_file.read().split('\n')

                # decode
                focal = np.fromstring(cam_args[1], dtype=float, sep=' ')
                pp = np.fromstring(cam_args[3], dtype=int, sep=' ')
                res = np.fromstring(cam_args[5], dtype=int, sep=' ')
                distortion = np.fromstring(cam_args[7], dtype=float, sep=' ')
                transform = np.matrix('{}; {}; {}; {}'.format(cam_args[12], cam_args[13], cam_args[14], cam_args[15]))

                # reference from yajie
                # The focal length in camera is not correspondent to 935x1400, which is the default img size 
                # to obtain the real focal length when rendering the training data,
                # we should multiply by the ratio:
                # camAspect = 3482.0 / 5218.0;
                # TEXTURE_WIDTH = 1400;
                # TEXTURE_HEIGHT = 1400;
                # VIEW_HEIGHT = TEXTURE_HEIGHT;
                # VIEW_WIDTH = floor(VIEW_HEIGHT * camAspect)+1;
                # SETTING_SIZE_X = 3482;
                # SETTING_SIZE_Y = 5218;
                # ratio = VIEW_HEIGHT / SETTING_SIZE_Y; 
                # For example, if the focal_length in the file is
                # #focal length 
                # 1773.580780 1773.580780,
                # then the actual focal length should be 
                # actual_focal_length = focal_length * ratio

                def hwf2list(res, focal):
                    # for all 1259 camera calibrations of given images, f_x == f_y
                    focal = focal * 1400/5218
                    return [1400, 935, focal[0]]

                def transform2list(transform):
                    transform_list = []
                    for row in np.asarray(transform):
                        transform_list.append(row.tolist())
                    return transform_list

                def sh2list(environ):
                    sh_file_name = sh_order[environ-1]
                    sh_name = os.path.splitext(sh_file_name)[0]
                    with open('{}/original_sh/{}.txt'.format(sh_folder_path, sh_name)) as sh_file:
                        sh_txt = sh_file.read().strip()
                        sh = np.matrix(sh_txt.replace('\n', ';'))
                        sh_list = []
                        for row in np.asarray(sh)[:4]:
                            sh_list.append(row.tolist())
                        return sh_list

                out_json['frames'].append({
                    'file_path': os.path.join(r, file),
                    'hwf': hwf2list(res, focal),
                    'transform_matrix': transform2list(transform),
                    'sh': sh2list(environ)
                })
                print('{}/{} is finished'.format(len(out_json['frames']), len(f)))

# output to json
with open('{}/transforms.json'.format(output_path), 'w') as out_file:
    json.dump(out_json, out_file, indent=4)