# cubemap_decompose_hdr2png
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is used to read an high dynamic range environment texture in equirectangular format, 
# convert to cubemap in composed and decomposed format
###########################
# Input Data Hierarchy:
# ./hdr
# ├── 03-Ueno-Shrine_3k.hdr
# ├── 10-Shiodome_Stairs_3k.hdr
# ...
###########################
# Output Data Hierarchy:
# ./png
# ├── cubemap_composed
# │   ├── 03-Ueno-Shrine_3k.jpg
# |   ...
# ├── cubemap_decomposed
# │   ├── 03-Ueno-Shrine_3k
# │   │   ├── negx.jpg
# │   │   ├── negy.jpg
# │   │   ├── negz.jpg
# │   │   ├── posx.jpg
# │   │   ├── posy.jpg
# │   │   └── posz.jpg
# |   ...
# └─── equirectangular
#     ├── 03-Ueno-Shrine_3k.jpg
#     ...
###########################

import cv2
import py360convert
import numpy as np
import os

if __name__ == "__main__":
    # define path
    hdr_folder = 'D:/data/lightProbe/Original/hdr/'
    png_folder = 'D:/data/lightProbe/Original/png/'
    format = '.jpg'

    # walk through
    for r, d, f in os.walk(hdr_folder):
        for file in f:
            if '.hdr' in file:
                filename = os.path.splitext(file)[0]
                hdr_path = os.path.join(r, file)
                # e.g.: "D:/data/lightProbe/Original/hdr/03-Ueno-Shrine_3k.hdr"

                # read hdr file
                hdr = cv2.imread(hdr_path, flags=cv2.IMREAD_ANYDEPTH)

                # convert to 6 sided cube map
                hdr_cubemap = py360convert.e2c(hdr, face_w=2048, mode='bilinear', cube_format='dice')
                hdr_cubes = py360convert.e2c(hdr, face_w=2048, mode='bilinear', cube_format='dict')

                # convert to ldr
                img_equirectangular = np.clip(hdr * 255, 0, 255).astype('uint8')
                img_cubemap = np.clip(hdr_cubemap * 255, 0, 255).astype('uint8')
                img_posx = np.clip(hdr_cubes['R'] * 255, 0, 255).astype('uint8')
                img_negx = np.clip(hdr_cubes['L'] * 255, 0, 255).astype('uint8')
                img_posy = np.clip(hdr_cubes['U'] * 255, 0, 255).astype('uint8')
                img_negy = np.clip(hdr_cubes['D'] * 255, 0, 255).astype('uint8')
                img_posz = np.clip(hdr_cubes['F'] * 255, 0, 255).astype('uint8')
                img_negz = np.clip(hdr_cubes['B'] * 255, 0, 255).astype('uint8')

                # output equirectangular
                path_equirectangular = png_folder + 'equirectangular/'
                os.makedirs(path_equirectangular, exist_ok=True)
                cv2.imwrite(path_equirectangular + filename + format, img_equirectangular)
                print('Equirectangular for', filename, 'saved')

                # output cubemap
                path_cubemap = png_folder + 'cubemap_composed/'
                os.makedirs(path_cubemap, exist_ok=True)
                cv2.imwrite(path_cubemap + filename + format, img_cubemap)
                print('Cubemap for', filename, 'saved')

                # output decomposed cube
                path_decompose = png_folder + 'cubemap_decomposed/' + filename + '/'
                os.makedirs(path_decompose, exist_ok=True)
                cv2.imwrite(path_decompose + 'posx' + format, cv2.flip(img_posx, 1))
                cv2.imwrite(path_decompose + 'negx' + format, img_negx)
                cv2.imwrite(path_decompose + 'posy' + format, cv2.flip(img_posy, 0))
                cv2.imwrite(path_decompose + 'negy' + format, img_negy)
                cv2.imwrite(path_decompose + 'posz' + format, img_posz)
                cv2.imwrite(path_decompose + 'negz' + format, cv2.flip(img_negz, 1))
                print('Decomposed cubemap for', filename, 'saved')