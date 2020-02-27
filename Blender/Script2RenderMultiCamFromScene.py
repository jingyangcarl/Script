import bpy
import os
from mathutils import Matrix, Vector
import numpy

# blender 2.8+

#---------------------------------------------------------------
# 3x4 P matrix from Blender camera
#---------------------------------------------------------------

# Build intrinsic camera parameters from Blender camera data
#
# See notes on this in 
# blender.stackexchange.com/questions/15102/what-is-blenders-camera-projection-matrix-model
def get_K_from_blender(camd):
    f_in_mm = camd.lens
    scene = bpy.context.scene
    resolution_x_in_px = scene.render.resolution_x
    resolution_y_in_px = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100
    sensor_width_in_mm = camd.sensor_width
    sensor_height_in_mm = camd.sensor_height
    pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
    if (camd.sensor_fit == 'VERTICAL'):
        # the sensor height is fixed (sensor fit is horizontal), 
        # the sensor width is effectively changed with the pixel aspect ratio
        s_u = resolution_x_in_px * scale / sensor_width_in_mm / pixel_aspect_ratio 
        s_v = resolution_y_in_px * scale / sensor_height_in_mm
    else: # 'HORIZONTAL' and 'AUTO'
        # the sensor width is fixed (sensor fit is horizontal), 
        # the sensor height is effectively changed with the pixel aspect ratio
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        s_u = resolution_x_in_px * scale / sensor_width_in_mm
        s_v = resolution_y_in_px * scale * pixel_aspect_ratio / sensor_height_in_mm


    # Parameters of intrinsic calibration matrix K
    alpha_u = f_in_mm * s_u
    alpha_v = f_in_mm * s_v
    u_0 = resolution_x_in_px * scale / 2
    v_0 = resolution_y_in_px * scale / 2
    skew = 0 # only use rectangular pixels

    K = Matrix(
        ((alpha_u, skew,    u_0),
        (    0  , alpha_v, v_0),
        (    0  , 0,        1 )))
    return K

# Returns camera rotation and translation matrices from Blender.
def get_RT_from_blender(cam):
    T, R = cam.matrix_world.decompose()[0:2]
    return T, R

def get_3x4_P_matrix_from_blender(cam):
    K = get_K_from_blender(cam.data)
    T, R = get_RT_from_blender(cam)
    return K, T, R

#---------------------------------------------------------------
# main
#---------------------------------------------------------------
outputPath = '/home/ICT2000/jyang/Documents/Project/DepthNoise/rendered_clean/'
outputFormat = '.png'
cameras_RT = {}
cameras_K = {}
cameras = bpy.data.cameras

# loop through each camera
for i, camera in enumerate(cameras) : 
    # debug purpose
    
    # get current camera
    camera = bpy.context.scene.objects[camera.name]
    print('Render using camera: ' + camera.name)
    
    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Make the current camera an active object
    bpy.context.view_layer.objects.active = camera
    
    # select the current camera
    camera.select_set(True)
    
    # set active object as cameratype
    bpy.context.scene.camera = camera
    
    # set path to save rendered results
    outputFile = outputPath + camera.name + outputFormat
    
    ## render image
    print('Rendering model ' + camera.name)
    bpy.ops.render.render()
    
    ## save RGB image
    if 'RGB' in camera.name:
        bpy.data.images['Viewer Node'].save_render(outputFile)
    ## save Depth image
    if 'IR' in camera.name:
        bpy.data.images['Render Result'].save_render(outputFile)
    
    print("Image saved at" + bpy.context.scene.render.filepath)
    
    # get K, R, T and print
    K, T, R = get_3x4_P_matrix_from_blender(camera)
    print(K)
    print(T)
    print(R)
    
    # save Ks, and RTs
    cameras_K[camera.name] = numpy.matrix(K).A1.tolist()
    cameras_RT[camera.name] = numpy.concatenate((R, T))[None].flatten()
    
    # save
    numpy.savetxt(outputPath+camera.name+'_K.txt', cameras_K[camera.name])
    print('intrinsic parameter saved')
    numpy.savetxt(outputPath+camera.name+'_RT.txt', cameras_RT[camera.name])
    print('extrinsic parameter saved')
    
# save RTs and Ks
numpy.savetxt(outputPath+'intrinsic.txt', list(cameras_K.values()))
numpy.savetxt(outputPath+'extrinsic.txt', list(cameras_RT.values()))
