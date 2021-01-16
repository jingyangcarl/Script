# equirectangular_exr_mirror
###########################
# Environment
# Python 3.7.4
###########################
# Description:
# This script is used to read an high dynamic range environment texture in equirectangular format and mirror it.
# Reference: 
# https://stackoverflow.com/questions/58022922/mirror-image-in-python
###########################
# Input Data Hierarchy:
# ./exr
# ├── 03-Ueno-Shrine_3k.hdr
# ├── 10-Shiodome_Stairs_3k.hdr
# ...
###########################
# Output Data Hierarchy:
# ./exr_mirror
# ├── 03-Ueno-Shrine_3k.exr
# ├── 10-Shiodome_Stairs_3k.exr
# ...
###########################

import imageio
import os

if __name__=="__main__":
    # define path
    exr_folder = 'D:/data/lightProbe/Original/exr/'
    exr_mirror_folder = 'D:/data/lightProbe/Original/exr_mirror/'

    # create exr_mirror folder
    os.makedirs(exr_mirror_folder)

    # walk through
    for r, d, f in os.walk(exr_folder):
        for file in f:
            if '.exr' in file:
                filename = os.path.splitext(file)[0]
                exr_path = os.path.join(r, file)
                # e.g.: "D:/data/lightProbe/Original/exr/03-Ueno-Shrine_3k.exr"

                # read exr file
                exr = imageio.imread(exr_path)

                # save exr_mirror file
                imageio.imwrite(exr_mirror_folder + filename + '.exr', exr[:,::-1,:])
                print('flipping completed:', filename)