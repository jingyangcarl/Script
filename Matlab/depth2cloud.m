function pcloud = depth2cloud(depth, intrinsic)
%% depthToCloud.m - Convert depth image into 3D point cloud
% Input: 
% depth - the normalized depth image;
% intrinsic - the intrinsic matrix of which generates the depth image;
%
% Output:
% pcloud - the point cloud, where each channel is the x, y, and z euclidean coordinates respectively.

% Author: Jing Yang

%% set parameter
[height, width] = size(depth);
f = 26; % focal length in real world unit, mm;
fx = intrinsic(1); % focal length in pixels along x direction;
fy = intrinsic(5); % focal length in pixels along y direction;
ppx = intrinsic(3); % principal point x;
ppy = intrinsic(6); % principal point y;
px = f/fx; % pixel size in real world unit along x direction, mm;
py = f/fy; % pixel size in real world unit along y direction, mm;

%% initialization
pcloud = zeros(height,width,3);
xgrid = ones(height,1)*(1:width) - ppx;
ygrid = (1:height)'*ones(1,width) - ppy;
zgrid = double(depth)*2.0 + 0.5;

%% convert depth image to 3d point clouds based on the real distance
% reference: https://www.mathworks.com/help/vision/ug/camera-calibration.html
% fx, fy are focal length in pixels, which equal to F/px and F/py.
% px and py are size of the pixel in world units, leading to: 
% (length in pixel) / (focal length in pixel) = (length in meter) / (depth in meter )

pcloud(:,:,1) = (xgrid.*zgrid)/fx;
pcloud(:,:,2) = (ygrid.*zgrid)/fy;

% with perspective correction
alpha_x = 1.0; alpha_y = 1.0;
pcloud(:,:,3) = (f*zgrid)./sqrt(f.^2 + alpha_x * (px*xgrid).^2 + alpha_y * (py*ygrid).^2);
