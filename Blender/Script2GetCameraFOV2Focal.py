# start with the initial blender scene
import bpy
import math
C = bpy.context
D = bpy.data

# refer to blender Camera: https://docs.blender.org/api/current/bpy.types.Camera.html
camera_obj = D.objects['Camera']
camera_fov_radius = camera_obj.data.angle
camera_fov_degree = camera_fov_radius / math.pi * 180
print("Camera FOV is", camera_fov_radius, "in radius and", camera_fov_degree, "in degree")
## Camera FOV is 0.6911112070083618 in radius and 39.597755335771296 in degree

# refer to blender Scene: https://docs.blender.org/api/current/bpy.types.Scene.html
scene_obj = C.scene
resolution_x = scene_obj.render.resolution_x
resolution_y = scene_obj.render.resolution_y

# refer to wiki angle of view: https://en.wikipedia.org/wiki/Angle_of_view
camera_focal = (resolution_x / 2) / math.tan(camera_fov_radius / 2)
## Camera focal length is 2666.6664748650437

# try to calculate from build in angle_x and angle_y
camera_fov_x = camera_obj.data.angle_x
camera_focal_x = (resolution_x / 2) / math.tan(camera_fov_x / 2)
camera_fov_y = camera_obj.data.angle_y
camera_focal_y = (resolution_y / 2) / math.tan(camera_fov_y / 2)
print("Camera focal length is", camera_focal)
print("Camera focal length calculated from x is", camera_focal_x)
print("Camera focal length calculated from y is", camera_focal_y)
## Camera focal length calculated from x is 2666.6664748650437
## Camera focal length calculated from y is 2250.0000113880437