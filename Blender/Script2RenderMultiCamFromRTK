import bpy
import numpy as np
import mathutils

plyFilePath = '/home/ICT2000/jyang/Documents/Data/rgbd-scenes-v2/pc/01.ply'
#bpy.ops.import_mesh.ply(filepath=plyFilePath)

cameraFilePath = '/home/ICT2000/jyang/Documents/Data/rgbd-scenes-v2/pc/01.pose'
cameraTable = np.loadtxt(cameraFilePath)
cameras_r = cameraTable[:,0:4]
cameras_xyz = cameraTable[:,4:7]

cameras = {}
camera_objs = {}

# add cameras
for i in range(0, cameraTable.shape[0], 1):
    orient_matrix = None
    matrix = None
    print(i)
    camera_name = 'Camera ' + str(i)
    # create camera
    cameras[i] = bpy.data.cameras.new(camera_name)
    cameras[i].lens = 30
    # create camera object
    camera_objs[i] = bpy.data.objects.new(camera_name, cameras[i])
    camera_objs[i].location = cameras_xyz[i]
    camera_objs[i].rotation_mode = 'XYZ'
    camera_objs[i].rotation_euler = mathutils.Quaternion(cameras_r[i]).to_euler('XYZ')
    camera_objs[i].scale = (0.3, 0.3, 0.3)
    camera_obj_name = camera_objs[i].name
    print(camera_obj_name)
    # add camera object to scene
    bpy.context.scene.collection.objects.link(camera_objs[i])

# add local transformation around x axis for 180 degrees
for i in camera_objs:
    # get camera_obj name
    camera_obj_name = camera_objs[i].name
    camera_objs[i].select_set(True)
    # get current rotation matrix
    orient_matrix = mathutils.Matrix(bpy.context.scene.collection.objects[camera_obj_name].matrix_world).to_3x3().normalized().transposed()
    # manually organize the rotation format (use orient_matrix from last line won't work)
    matrix = ((orient_matrix[0][0], orient_matrix[0][1], orient_matrix[0][2]), (orient_matrix[1][0], orient_matrix[1][1], orient_matrix[1][2]), (orient_matrix[2][0], orient_matrix[2][1], orient_matrix[2][2]))
    # rotate
    bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='LOCAL', orient_matrix=matrix, orient_matrix_type='LOCAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
# remove all cameras
for i in camera_objs:
    #bpy.context.scene.collection.objects.unlink(cameras_obj[i])
    pass
