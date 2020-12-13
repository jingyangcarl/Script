# equirectangular_hdr2exr
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is used to read an high dynamic range environment texture in equirectangular format, 
# convert from .hdr format to .exr format
###########################
# Input Data Hierarchy:
# ./hdr
# ├── 03-Ueno-Shrine_3k.hdr
# ├── 10-Shiodome_Stairs_3k.hdr
# ...
###########################
# Output Data Hierarchy:
# ./exr
# ├── 03-Ueno-Shrine_3k.exr
# ├── 10-Shiodome_Stairs_3k.exr
# ...
###########################

import imageio
import os

if __name__=="__main__":
    # define path
    hdr_folder = 'D:/data/lightProbe/Original/hdr/'
    exr_folder = 'D:/data/lightProbe/Original/exr/'

    # create exr folder
    os.makedirs(exr_folder)

    # walk through
    for r, d, f in os.walk(hdr_folder):
        for file in f:
            if '.hdr' in file:
                filename = os.path.splitext(file)[0]
                hdr_path = os.path.join(r, file)
                # e.g.: "D:/data/lightProbe/Original/hdr/03-Ueno-Shrine_3k.hdr"

                # read hdr file
                hdr = imageio.imread(hdr_path, format='HDR-FI')

                # save exr file
                imageio.imwrite(exr_folder + filename + '.exr', hdr)
                print('Converting completed:', filename)