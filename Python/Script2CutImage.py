# Script2CutImage
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is used to cut image to patches in order
###########################
# Input Data Hierarchy:
# ./RawData
# ├───LightStageData
# │   └───SpecularUnlit
# │           20181212_LocHuynh_00_specular_unlit.exr
# │           20181212_LocHuynh_01_specular_unlit.exr
# │           20181212_LocHuynh_02_specular_unlit.exr
# │			...
# │
# └───OldLightStageData
#     └───SpecularUnlit
#             201170115_Adair_00_1_specular_unlit.exr
#             201170115_Adair_01_0_specular_unlit.exr
#             201170115_Adair_02_0_specular_unlit.exr
#             ...
###########################
# Output Data Hierarchy:
# ./ImageCut48
# ├───LightStageData
# │   └───SpecularUnlit
# │       ├───20181212_LocHuynh_00_specular_unlit
# │       │       patch_0_0.exr
# │       │       patch_0_144.exr
# │       │       patch_0_192.exr
# │       │       ...
# │       ├───20181212_LocHuynh_01_specular_unlit
# │       │       patch_0_0.exr
# │       │       patch_0_144.exr
# │       │       patch_0_192.exr
# │       │       ...
# │ 		...
# └───OldLightStageData
#     └───SpecularUnlit
#         ├───201170115_Adair_00_1_specular_unlit
#         │       patch_0_0.exr
#         │       patch_0_144.exr
#         │       patch_0_192.exr
#         │       ...
#         ├───201170115_Adair_01_0_specular_unlit
#         │       patch_0_0.exr
#         │       patch_0_144.exr
#         │       patch_0_192.exr
#         │       ...
#         ...
###########################

import imageio
import os
import cv2
from PIL import Image

def load_image(filename):
    return imageio.imread(filename, format='EXR-FI')

def save_image(filePath, image, skip_if_exist=False):
    if skip_if_exist and os.path.exists(filePath):
        return
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    imageio.imwrite(filePath, image, format='EXR-FI')

# main function
if __name__ == "__main__":

    # define file path 
    # inputFile = "F:/Data/FaceEncoding/RawData/LightStageData/SpecularUnlit/20181212_LocHuynh_00_specular_unlit.exr"
    # outputFolder = "F:/Data/FaceEncoding/GeneratedData/ImageCut48/LightStageData/SpecularUnlit/20181212_LocHuynh_00_specular_unlit"

    inputRootFolder = "F:/Data/FaceEncoding/RawData/"
    outputRootFolder = "F:/Data/FaceEncoding/GeneratedData/ImageCut48/"

    # walk through
    for r, d, f in os.walk(inputRootFolder):
        for file in f:
            if '.exr' in file:
                filePath = os.path.join(r, file)
                # e.g.: "F:/Data/FaceEncoding/RawData/LightStageData/SpecularUnlit/20181212_LocHuynh_00_specular_unlit.exr"

                # read exr file
                if not os.path.isfile(filePath):
                    print(filePath + ' IS NOT A VALID FILE')
                image4096 = load_image(filePath)

                # resize image from 4096 * 4086 to 1024 * 1024
                inputSize = image4096.shape
                if inputSize[0] != 4096 and inputSize[1] != 4096:
                    print('Input size is not 4096 by 4096')
                outputSize = (int(inputSize[0]/4), int(inputSize[1]/4))
                image1024 = cv2.resize(image4096, outputSize)

                # set output image path 
                relativePath = filePath[len(inputRootFolder):]
                # e.g. "LightStageData/SpecularUnlit/20181212_LocHuynh_00_specular_unlit.exr"
                outputFolder = outputRootFolder + os.path.splitext(relativePath)[0] + '/'
                # e.g. "F:/Data/FaceEncoding/GeneratedData/ImageCut48/LightStageData/SpecularUnlit/20181212_LocHuynh_00_specular_unlit/"

                # crop images from 1024 * 1024 to 48 * 48
                patchSize = 48
                for i in range(0, 1024-patchSize, patchSize):
                    for j in range(0, 1024-patchSize, patchSize):

                        # crop image
                        image48 = image1024[i:i+patchSize, j:j+patchSize]
                        print('Current Patch in ' + filePath + ': \t[' + str(i) + ' : ' + str(i+patchSize) + ', ' + str(j) + ' : ' + str(j+patchSize) + ']')

                        outputFilePath = outputFolder + '/patch_' + str(i) + '_' + str(j) + '.exr'
                        
                        # save image
                        save_image(outputFilePath, image48)

    cv2.waitKey(0)

    cv2.destroyAllWindows()