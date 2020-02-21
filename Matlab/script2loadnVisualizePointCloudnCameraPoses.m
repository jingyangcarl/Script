clear all;

% reference: https://rgbd-dataset.cs.washington.edu/
%% read camera poses
cameras_table = readtable('01.pose', 'Format', '%f%f%f%f%f%f%f', 'FileType', 'text');
cameras = cameras_table{:,:};
cameras_q = cameras(:, 1:4);
cameras_xyz = cameras(:,5:7);

%% read depth image
depth = imread('00000-depth.png');
pcloud_depth = depthToCloud(depth);
% depthToCloud can be downloaded here: https://rgbd-dataset.cs.washington.edu/software.html

%% read scene point cloud
pcloud_scene = pcread('01.ply');

%% show scene cloud and cameras
pcshow(pcloud_scene);
hold on;
pcshow(cameras_xyz, 'bo');
step = uint16(size(cameras, 1)/10); % the larger the denominator, the more cameras will be displayed
for i = 1:step:size(cameras, 1)
    plotCamera('Location', cameras_xyz(i,:), 'Orientation', quat2rotm(cameras_q(i,:))', 'Size', 0.05)
end