

import os
import re

inputModelFolder = 'E:/Data/MIXAMO/DataGenerated_FrameShotsWithTexture/'

files = []
# walk through all files in inputModelFolder and find all '.mtl' file
# r = root, d = directories, f = files
for r, d, f in os.walk(inputModelFolder):
    for file in f:
        if '.mtl' in file:

            # found '.mtl' files
            currentFile = os.path.join(r, file)
            files.append(currentFile)

            # print current file
            print (currentFile)
            
            # find model index in path
            modelNums = re.search(r'model_\d*', currentFile)
            modelNum = re.search(r'\d+', modelNums.group(0)).group(0)
            
            # read .mtl file
            with open(os.path.join(r, file)) as mtlFile:
                content = mtlFile.read().splitlines()
            
            # '.mtl' file is export from maya, which is organized in
            # newmtl ...
            # illumn ...
            # Kd ...
            # Ka ...
            # Tf ...
            # Ni ...
            # Ks ...
            # Ns ...
            # where map_Kd and map_Ka should be added after Ns
            part = ''
            for index, line in enumerate(content):
                words = line.split()
                if (words[0] == 'newmtl'):
                    # remove extra character
                    part = words[1]
                    part = re.sub(r'SG\d*', '', part)
                    if (part == 'Bottoms'):
                        part = 'Bottom'
                    if (part == 'Eyelashes'):
                        part = 'Body'
                    if (part == 'default1'):
                        part = 'Body'
                    if (part == 'Hair'):
                        part = 'Hair'
                    if (part == 'Shoes'):
                        part = 'Shoes'
                    if (part == 'Tops'):
                        part = 'Top'
                if (words[0] == 'Ns'):
                    # add diffuse map and specular map
                    content.insert(index+1, 'map_Kd texture/FuseModel_' + modelNum + '_' + part + '_Diffuse.png')
                    content.insert(index+2, 'map_Ks texture/FuseModel_' + modelNum + '_' + part + '_Specular.png')
            
            # write file
            #outputFile = open(os.path.join(r, 'test.mtl'), 'w')
            outputFile = open(currentFile, 'w')
            for line in content:
                outputFile.write(line + '\n')
            outputFile.close()
