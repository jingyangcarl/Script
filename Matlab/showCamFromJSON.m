function [transform_matrix_list, camera_list] = showCamFromJSON(f_name)
%% showCamFromJSON.m - load transformation matrix from JSON and plot
% Input:
% Output:

%Author: Jing Yang

%% read json file
f_id = fopen(f_name);
f_raw = fread(f_id, inf);
f_str = char(f_raw');
fclose(f_id);
json_obj = jsondecode(f_str);

%% init data
len = length(json_obj.frames);
file_path_list = string(len);
rotation_list = zeros(1, len);
transform_matrix_list = zeros(4,4,len);
camera_list = vision.graphics.Camera.empty;

%% fill in data
for i = 1:len
    file_path_list(i) = json_obj.frames(i).file_path;
    rotation_list(i) = json_obj.frames(i).rotation;
    transform_matrix_list(:,:,i) = json_obj.frames(i).transform_matrix;
end

%% plot cameras
% the initial position of Blender camera is pointing at negative z axis;
% the initial position of Matlab camera is pointing at positive z axis;
% Blender and Matlab both use the right handed coordination system, 
% which means we have to do y flip before apply the quaternion rotation;
% that is to say, we need to multiply [0.0, 0.0, 1.0, 0.0];
% moreover, the upvector of the two camera system is also flipped,
% which means we have to do z flip as well;

% Tip: If r is a rotation matrix, det(r) should be 1, inv(r) should equals
    % to r', since r is a orthogonal matrix;

% show cam
for i = 1:len
    t = transform_matrix_list(1:3,4,i)';
    r = quaternion(rotm2quat(transform_matrix_list(1:3,1:3,i))) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]);
    
    colormap default;
    cmap = colormap;
    
    camera_list(i) = plotCamera('Label', file_path_list(i), 'Location', t, 'Orientation', quat2rotm(r)', 'Size', 0.05, 'Color', cmap(round(i/len*size(cmap, 1)),:));
    hold on;
end

% configure display
axis equal;
grid on;
xlabel('x');
ylabel('y');
zlabel('z');
colorbar;