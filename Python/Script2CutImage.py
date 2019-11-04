import imageio
import os
import cv2

def load_image(filename):
    return imageio.imread(filename, format='EXR-FI')

# main function
if __name__ == "__main__":
    filePath = "F:\\Data\\FaceEncoding\\RawData\\LightStageData\\SpecularUnlit\\20181212_LocHuynh_00_specular_unlit.exr"
    if not os.path.isfile(filePath):
        print('The filePath is not a path')
    image = load_image(filePath)