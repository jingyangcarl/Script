# equirectangular_exr_downsample
###########################
# Environment
# Python 3.7.4
###########################
# Description:
# This script is used to read an high dynamic range environment texture in equirectangular format and downsample it.
###########################
# Input Data Hierarchy:
# ./exr
# ├── 03-Ueno-Shrine_3k.hdr
# ├── 10-Shiodome_Stairs_3k.hdr
# ...
###########################
# Output Data Hierarchy:
# ./exr_downsample
# ├── 03-Ueno-Shrine_3k.exr
# ├── 10-Shiodome_Stairs_3k.exr
# ...
###########################

import imageio
import os

if __name__=="__main__":
    # define path
    exr_folder = 'D:/data/lightProbe/Original/exr/'
    exr_downsample_folder = 'D:/data/lightProbe/Original/exr_downsample/'
    down_step = 100

    # create exr_mirror folder
    os.makedirs(exr_downsample_folder)

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
                imageio.imwrite(exr_downsample_folder + filename + '.exr', exr[::down_step,::down_step,:])
                print('downsample completed:', filename)