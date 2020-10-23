# Script2ComposeSkybox
###########################
# Environment
# Python 3.7.4
###########################
# Description
# This script is used to compose 6 sided skybos into one
###########################
# Input Data Hierarchy:
# ./Cubemap_decomposed
# ├───00
# │       negx.jpg
# │       negy.jpg
# │       negz.jpg
# │       posx.jpg
# │       posy.jpg
# │       posz.jpg
# │
# ├───01
# │       negx.jpg
# │       negy.jpg
# │       negz.jpg
# │       posx.jpg
# │       posy.jpg
# │       posz.jpg
# │
# ...
###########################
# Output Data Hierarchy:
# ./Cubemap_composed
# ├───00
# │       skybox.jpg
# │
# ├───01
# │       skybox.jpg
# │
# ...
###########################

from PIL import Image
import os

inputRootFolder = 'F:/Project/Visual Studio/SphericalHarmonicsLighting/SphericalHarmonicsLighting/Resources/Skybox/SixSide'
outputRootFolder = 'F:/Project/Visual Studio/SphericalHarmonicsLighting/SphericalHarmonicsLighting/Resources/Skybox/SixSideCompose'

for r, d, f in os.walk(inputRootFolder):
    for dir in d:
        # change the current working directory
        os.chdir(os.path.join(r, dir))

        # read 6 images
        image_negx = Image.open('negx.jpg')
        image_negy = Image.open('negy.jpg')
        image_negz = Image.open('negz.jpg')
        image_posx = Image.open('posx.jpg')
        image_posy = Image.open('posy.jpg')
        image_posz = Image.open('posz.jpg')
        width, height = image_negx.size

        # prepare a white image
        image_white = Image.new('RGB', (width, height), (255, 255, 255))

        # prepare new image
        image = Image.new('RGB', (4 * width, 3 * height))

        # line 1
        image.paste(image_white, (0 * width, 0 * height))
        image.paste(image_posy, (1 * width, 0 * height))
        image.paste(image_white, (2 * width, 0 * height))
        image.paste(image_white, (3 * width, 0 * height))

        # line 2
        image.paste(image_negx, (0 * width, 1 * height))
        image.paste(image_posz, (1 * width, 1 * height))
        image.paste(image_posx, (2 * width, 1 * height))
        image.paste(image_negz, (3 * width, 1 * height))

        # line 3
        image.paste(image_white, (0 * width, 2 * height))
        image.paste(image_negy, (1 * width, 2 * height))
        image.paste(image_white, (2 * width, 2 * height))
        image.paste(image_white, (3 * width, 2 * height))

        # create output directories
        outputDir = os.path.join(outputRootFolder, dir)
        os.makedirs(outputDir, exist_ok=True)

        # save image
        image.save(outputDir + '\skybox.jpg', format='JPEG')
        print(outputDir + '\skybox.jpg saved successfully')