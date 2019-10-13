import os
import re

projectFolder = 'D:/CSCI580/Homework4/'
projectFolder = 'D:/Code/SphericalHarmonicsLighting'

#############################################################
# fill filePathDic, fileHierarchyDic
# where filePathDic is used to save files absolute path on the machine,
# and fileHierarchyDic is used to save solution hierarchy path as shown in Visual Studio Solution Viewer

# generate project tree
filePathDic = {}
fileHierarchyDic = {}

# set file format to be processed
extension = {
    '.h',
    '.cpp'
}

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
                            # for leaf nodes
                            # extract leafFile from <... Include="leafFile">
                            leafFile = re.search(r'\".*\"',line).group(0).replace('\"', '', 2)
                            # extract pathToLeaf from <Filter>pathToLeaf</Filter>
                            pathToLeaf = re.search(r'>.*<', content[index+1]).group(0).replace('>', '').replace('<', '/')
                            # replace '\\' with '/'
                            pathToLeaf = pathToLeaf.replace('\\', '/')

                            # add to hierarchy dictionary
                            leafFileName, leafFileExtension = os.path.splitext(leafFile)
                            if leafFileExtension in extension:
                                fileHierarchyDic[leafFile.lower()] = pathToLeaf + leafFile
                        else:
                            # other than leaf nodes
                            node = re.search(r'\".*\"', line).group(0).replace('\"', '', 2)
        # add to path dictionary
        if fileExtension in extension:
            filePathDic[file.lower()] = os.path.join(r, file)

#############################################################
# generate solution hierarchy tree using fileHierarchyDic

class TreeNode(object):
    def __init__(self, name = None, children = None):
        self.name = name
        self.children = children

hierarchy = TreeNode('Root')
for file in fileHierarchyDic:
    currentNode = hierarchy
    nodeNames = fileHierarchyDic[file].split('/')
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

# Description:
# This function is used to generate markdown content of a cpp source file in hierarchy structure
# Input:
# @ fileName: input cpp source file
# @ markdown: output markdown content
# Output:
# @ void: return value
def generateCppMarkDown(fileName, markdown):

    filePath = filePathDic[fileName.lower()]

    # concat comments
    description = ''
    function = ''

    # read .cpp file and extract descriptions
    with open(filePath) as cppFile:
        content = cppFile.read().splitlines()

        for index, line in enumerate(content):
            # loop through all functions
            if line.strip() == '/*':
                # the comments may be a description comments
                if 'Description:' in content[index+1]:
                    # locate the number of lines of description part
                    length = 0
                    for i in range(2, 20):
                        if 'Input:' in content[index + i]:
                            length = i
                            break
                        if '*/' in content[index + i]:
                            length = i
                            break
                    
                    for i in range(2, length):
                        description += content[index + i].strip()
                        if not description.endswith(';'):
                            description += ';'
                        #markdown.append(description)

            if line.strip() == '*/':
                # locate function statement
                if '::' in content[index+1]:
                    function = content[index+1].replace('{', '').strip()
                    function = function.replace(' :', '').strip()
                    markdown.append(function + ': ' + description)
                    description = ''


def traversal(node, layerStr, markdown):
    if node is None: return
    if node.children is None:
        # traversal leaf node
        subMarkdown = []
        markdown.append(layerStr + ' ' + node.name)
        generateCppMarkDown(node.name, subMarkdown)

        for line in subMarkdown:
            markdown.append(layerStr + '> ')
            markdown.append(layerStr + '> ' + line)

        markdown.append(layerStr + ' ')
        return
    
    # traversal the node
    markdown.append(layerStr + ' ' + node.name)
    markdown.append(layerStr + ' ')

    # traveral through child node
    for childNode in node.children:
        traversal(childNode, layerStr + '>', markdown)

markdown = []
traversal(hierarchy, '', markdown)
for line in markdown:
    print(line)
