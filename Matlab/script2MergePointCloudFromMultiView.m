clear all;
close all;

%% set parameters
input_dir = 'D:/Data/MIXAMO/generated_frames_rendered/all/640_480/model_0/model_0_anim_0/model_0_anim_0_f0/';
height = 480;
width = 640;
view_num = 16;

%% initialization
% intrinsics
ks_table = readtable(strcat(input_dir,'intrinsic.txt'), 'Format', '%f%f%f%f%f%f%f%f%f', 'FileType', 'text');
ks = ks_table{:,:};
ks_depth_left = ks(1:3:end, :);
ks_depth_right = ks(2:3:end, :);
ks_color = ks(3:3:end, :);
clear ks_table;

% extrinsics
rts_table = readtable(strcat(input_dir,'extrinsic.txt'), 'Format', '%f%f%f%f%f%f%f', 'FileType', 'text'); % r_w, r_x, r_y, r_z, t_x, t_y, t_z
rts = rts_table{:,:};
rts_depth_left = rts(1:3:end, :);
rts_depth_right = rts(2:3:end, :);
rts_color = rts(3:3:end, :);
clear rts_table;

% depth and color images
images_depth_left_png = zeros(height, width, view_num, 'uint16');
images_depth_left_exr = zeros(height, width, view_num, 'single');
images_depth_right_png = zeros(height, width, view_num, 'uint16');
images_depth_right_exr = zeros(height, width, view_num, 'single');
images_color = zeros(height, width, 3, view_num, 'uint8');
for i = 1:view_num
    images_depth_left_png(:,:,i) = imread(strcat(input_dir, 'D415.', sprintf('%02d',i), '.IR.L.png'));
    images_depth_left_exr(:,:,i) = rgb2gray(exrread(strcat(input_dir, 'D415.', sprintf('%02d',i), '.IR.L.exr')));
    images_depth_right_png(:,:,i) = imread(strcat(input_dir, 'D415.', sprintf('%02d',i), '.IR.R.png'));
    images_depth_right_exr(:,:,i) = rgb2gray(exrread(strcat(input_dir, 'D415.', sprintf('%02d',i), '.IR.R.exr')));
    images_color(:,:,:,i) = imread(strcat(input_dir, 'D415.', sprintf('%02d',i), '.RGB.png'));
end

% point cloud
pclouds_depth_left = zeros(height, width, 3, view_num, 'double');
pclouds_depth_left_transformed = zeros(height, width, 3, view_num, 'double');
pclouds_depth_right = zeros(height, width, 3, view_num, 'double');
pclouds_depth_right_transformed = zeros(height, width, 3, view_num, 'double');

%% plot cameras
% the initial position of Blender camera is pointing at negative z axis;
% the initial position of Matlab camera is pointing at positive z axis;
% Blender and Matlab both use the right handed coordination system, 
% which means we have to do y flip before apply the quaternion rotation;
% that is to say, we need to multiply [0.0, 0.0, 1.0, 0.0];
% moreover, the upvector of the two camera system is also flipped,
% which means we have to do z flip as well;

% show cam
for i = 1:view_num
    t_depth_left = rts_depth_left(i, end-2:end);
    t_depth_right = rts_depth_right(i, end-2:end);
    r_depth_left = quaternion(rts_depth_left(i, 1:4)) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]);
    r_depth_right = quaternion(rts_depth_right(i, 1:4)) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]);
    plotCamera('Label', sprintf('%02d',i), 'Location', t_depth_left, 'Orientation', quat2rotm(r_depth_left)', 'Size', 0.05, 'Color', [1 0 0]);
    plotCamera('Label', sprintf('%02d',i), 'Location', t_depth_right, 'Orientation', quat2rotm(r_depth_right)', 'Size', 0.05, 'Color', [0 0 1]); 
    hold on;
end

% configure display
axis equal;
grid on;
xlabel('x');
ylabel('y');
zlabel('z');

%% generate point cloud from depth
for i = 1:view_num
    pclouds_depth_left(:,:,:,i) = depth2cloud(images_depth_left_exr(:,:,i), ks_depth_left(i,:));
    pclouds_depth_right(:,:,:,i) = depth2cloud(images_depth_right_exr(:,:,i), ks_depth_right(i,:));
end

%% transform point cloud for merge
for i = 1:view_num
    t_depth_left = rts_depth_left(i, end-2:end);
    r_depth_left = quaternion(rts_depth_left(i, 1:4)) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]);
    rt_depth_left = rigid3d(quat2rotm(r_depth_left)', t_depth_left);
    pcloud_depth_left_transformed = pctransform(pointCloud(pclouds_depth_left(:,:,:,i)), rt_depth_left);
    pclouds_depth_left_transformed(:,:,:,i) = pcloud_depth_left_transformed.Location;
end

%% show transformed point cloud
for i = 1:1:16
    pcshow(pclouds_depth_left_transformed(:,:,:,i));
    hold on;
end

%% try here
% pc = pointCloud(pclouds_depth_left(:,:,:,1));
% r = quaternion(rts_depth_left(1, 1:4)) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]);
% t = rts_depth_left(1, end-2:end);
% rt = rigid3d(quat2rotm(r)', t);
% pc_out = pctransform(pc, rt);
% pcshow(pc_out);