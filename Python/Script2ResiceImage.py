import imageio
import os
import cv2

inputRootFolder = 'F:/Data/Calibration/Full Body Scan/1944'
outputRootFolder = 'F:/Data/Calibration/Full Body Scan/243'

for r, d, f in os.walk(inputRootFolder):
    for file in f:
        if '.jpg' in file:
            inputFilePath = os.path.join(r, file)
            # e.g. : 'F:/Data/Calibration/Full Body Scan - A Pose/2k\10_YukihiroIwayama.jpg'
            print(inputFilePath)

            # read file
            image_original = imageio.imread(inputFilePath, format='JPG')
            image_original_size = image_original.shape

            # resize file
            resizeFactor = 8
            image_resize = cv2.resize(image_original, (int(image_original_size[1]/resizeFactor), int(image_original_size[0]/resizeFactor)))

            # save file
            outputFilePath = os.path.join(outputRootFolder, file)
            if os.path.exists(outputFilePath) : continue
            imageio.imwrite(outputFilePath, image_resize, format='JPG')


