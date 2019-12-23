# Script2ResizeImage
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is used to resize image with a resizeFactor (larger than 1)
###########################
# Input Data Hierarchy:
# ./1944
# 101.jpg
# 102.jpg
# 103.jpg
# 104.jpg
# 105.jpg
# ...
###########################
# Output Data Hierarchy:
# ./243
# 101.jpg
# 102.jpg
# 103.jpg
# 104.jpg
# 105.jpg
# ...
###########################

import imageio
import os
import cv2

inputRootFolder = 'F:/Data/Calibration/Full Body Scan - A Pose/2464'
outputRootFolder = 'F:/Data/Calibration/Full Body Scan - A Pose/821'

resizeFactor = 3

for r, d, f in os.walk(inputRootFolder):
    for file in f:
        if '.jpg' in file:
            inputFilePath = os.path.join(r, file)
            # e.g. : 'F:/Data/Calibration/Full Body Scan - A Pose/2k\10_YukihiroIwayama.jpg'

            # read file
            image_original = imageio.imread(inputFilePath, format='JPG')
            image_original_size = image_original.shape

            # resize file
            image_resize = cv2.resize(image_original, (int(image_original_size[1]/resizeFactor), int(image_original_size[0]/resizeFactor)))
            print(inputFilePath + ' resize finished')

            # save file
            outputFilePath = os.path.join(outputRootFolder, file)
            if os.path.exists(outputFilePath) : continue
            imageio.imwrite(outputFilePath, image_resize, format='JPG')


