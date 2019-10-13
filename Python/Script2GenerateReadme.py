import os
import re

projectFolder = 'D:/CSCI580/Homework4/'

#############################################################
# fill sourceFilePath, headerFilePath, sourceFileHierarchy, headerFileHierarchy
# where sourceFilePath and headerFilePath are used to save files absolute path on the machine,
# and sourceFileHierarchy and headerFileHierarchy are used to save solution hierarchy path as shown in Visual Studio Solution Viewer

# generate project tree
sourceFilePath = {}
headerFilePath = {}
sourceFileHierarchy = {}
headerFileHierarchy = {}

# walk through all files in projectFolder and find all files
# r = root, d = directories, f = files
for r, d, f in os.walk(projectFolder):
    for file in f:
        # loop through all the files
        fileName, fileExtension = os.path.splitext(file)
        if fileExtension == '.filters':
            # read vcxproj.filters and generate solution hierarchy tree
            with open(os.path.join(r, file), encoding='utf-8') as filterFile:
                content = filterFile.read().splitlines()
                for index, line in enumerate(content):
                    if 'Include=' in line:
                        # the string after Include= is nodes in solution hierarchy
                        if 'Filter' in content[index+1]:
                            # the string
                            leafFile = re.search(r'\".*\"',line).group(0).replace('\"', '', 2)
                            pathToLeaf = re.search(r'>.*<', content[index+1]).group(0).replace('>', '').replace('<', '/')

                            leafFileName, leafFileExtension = os.path.splitext(leafFile)
                            if leafFileExtension == '.h':
                                headerFileHierarchy[leafFile] = pathToLeaf + leafFile
                            if leafFileExtension == '.cpp':
                                sourceFileHierarchy[leafFile] = pathToLeaf + leafFile
                        else:
                            #
                            node = re.search(r'\".*\"', line).group(0).replace('\"', '', 2)
                            head = os.path.split(node)[0]
                            tail = os.path.split(node)[1]
        if fileExtension == '.h':
            headerFilePath[file] = os.path.join(r, file)
        if fileExtension == '.cpp':
            sourceFilePath[file] = os.path.join(r, file)

#############################################################
# generate solution hierarchy tree using sourceFileHierarchy and headerFileHierarchy

class TreeNode(object):
    def __init__(self, name = None, children = None):
        self.name = name
        self.children = children

hierarchy = TreeNode('Root')
for file in headerFileHierarchy:
    currentNode = hierarchy
    nodeNames = headerFileHierarchy[file].split('/')
    for nodeName in nodeNames:
        # loop through all folder/file name in a path
        newNode = TreeNode(nodeName)
        if currentNode.children is None:
            # if the currentNode has no child, add newNode to children list and go depper
            currentNode.children = []
            currentNode.children.append(newNode)
            currentNode = newNode
        else:
            # if the currentNode has children, check if the newNode is already existed
            existance = False
            for childNode in currentNode.children:
                if childNode.name == nodeName:
                    # if the newNode is already existed, just go deeper
                    currentNode = childNode
                    existance = True
                    break
            
            # if the newNode is not existed, add newNode to the children list and go deeper
            if not existance: 
                currentNode.children.append(newNode)
                currentNode = newNode

for file in sourceFileHierarchy:
    currentNode = hierarchy
    nodeNames = sourceFileHierarchy[file].split('/')
    for nodeName in nodeNames:
        # loop through all folder/file name in a path
        newNode = TreeNode(nodeName)
        if currentNode.children is None:
            # if the currentNode has no child, add newNode to children list and go depper
            currentNode.children = []
            currentNode.children.append(newNode)
            currentNode = newNode
        else:
            # if the currentNode has children, check if the newNode is already existed
            existance = False
            for childNode in currentNode.children:
                if childNode.name == nodeName:
                    # if the newNode is already existed, just go deeper
                    currentNode = childNode
                    existance = True
                    break
            
            # if the newNode is not existed, add newNode to the children list and go deeper
            if not existance: 
                currentNode.children.append(newNode)
                currentNode = newNode

#############################################
# generate Readme content using preorder traversal
def traversal(node):
    if node is None: return
    if node.children is None:
        print(node.name)
        return
    for childNode in node.children:
        traversal(childNode)

traversal(hierarchy)