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
def get_calibration_matrix_K_from_blender(camd):
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
# 
# There are 3 coordinate systems involved:
#    1. The World coordinates: "world"
#       - right-handed
#    2. The Blender camera coordinates: "bcam"
#       - x is horizontal
#       - y is up
#       - right-handed: negative z look-at direction
#    3. The desired computer vision camera coordinates: "cv"
#       - x is horizontal
#       - y is down (to align to the actual pixel coordinates 
#         used in digital images)
#       - right-handed: positive z look-at direction
def get_3x4_RT_matrix_from_blender(cam):
    # bcam stands for blender camera
    R_bcam2cv = Matrix(
        ((1, 0,  0),
         (0, -1, 0),
         (0, 0, -1)))

    # Transpose since the rotation is object rotation, 
    # and we want coordinate rotation
    # R_world2bcam = cam.rotation_euler.to_matrix().transposed()
    # T_world2bcam = -1*R_world2bcam * location
    #
    # Use matrix_world instead to account for all constraints
    location, rotation = cam.matrix_world.decompose()[0:2]
    R_world2bcam = rotation.to_matrix().transposed()

    # Convert camera location to translation vector used in coordinate changes
    # T_world2bcam = -1*R_world2bcam*cam.location
    # Use location from matrix_world to account for constraints:     
    T_world2bcam = -1*R_world2bcam @ location

    # Build the coordinate transform matrix from world to computer vision camera
    R_world2cv = R_bcam2cv@R_world2bcam
    T_world2cv = R_bcam2cv@T_world2bcam

    # put into 3x4 matrix
    RT = Matrix((
        R_world2cv[0][:] + (T_world2cv[0],),
        R_world2cv[1][:] + (T_world2cv[1],),
        R_world2cv[2][:] + (T_world2cv[2],)
         ))
    return RT

def get_3x4_P_matrix_from_blender(cam):
    K = get_calibration_matrix_K_from_blender(cam.data)
    RT = get_3x4_RT_matrix_from_blender(cam)
    return K@RT, K, RT

#---------------------------------------------------------------
# main
#---------------------------------------------------------------
outputPath = 'F:\Project\Blender\CameraStage\Camera Stage V2.1\model\\'

cameraNames = {
    0 : 'D415.R(+22.5d).up',
    1 : 'D415.R(+67.5d).up',
    2 : 'D415.R(+112.5d).up',
    3 : 'D415.R(+157.5d).up',
    4 : 'D415.R(-157.5d).up',
    5 : 'D415.R(-112.5d).up',
    6 : 'D415.R(-67.5d).up',
    7 : 'D415.R(-22.5d).up',
    8 : 'D415.R(+22.5d).down',
    9 : 'D415.R(+67.5d).down',
    10 : 'D415.R(+112.5d).down',
    11 : 'D415.R(+157.5d).down',
    12 : 'D415.R(-157.5d).down',
    13 : 'D415.R(-112.5d).down',
    14 : 'D415.R(-67.5d).down',
    15 : 'D415.R(-22.5d).down',
}

for i in cameraNames : 
    # get current camera
    cameraName = cameraNames[i]
    camera = bpy.context.scene.objects[cameraName]
    print('Render using camera: ' + cameraName)
    
    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    
    # Make the current camera an active object
    bpy.context.view_layer.objects.active = camera
    
    # select the current camera
    camera.select_set(True)
    
    # set active object as camera
    bpy.context.scene.camera = camera
    
    # set path to save rendered results
    bpy.context.scene.render.filepath = outputPath + cameraName
    
    ## render image
    print('Rendering model ' + cameraName)
    bpy.ops.render.render(write_still=True)
    
    # get R, K, RT
    P, K, RT = get_3x4_P_matrix_from_blender(camera)
    numpy.savetxt(outputPath+cameraName+'_intrinsic.txt', numpy.matrix(K))
    print('intrinsic parameter saved')
    print(K)
    numpy.savetxt(outputPath+cameraName+'_extrinsic.txt', numpy.matrix(RT))
    print('extrinsic parameter saved')
    print(RT)
    
    