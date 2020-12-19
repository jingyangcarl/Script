%% spherical_texture_mapping.m
% Description: this code is used to map any equirectangular environmental
% map onto a sphere.

% Author: Jing Yang

clear all;
close all;
img_path = '/home/ICT2000/jyang/Documents/Data/ForJing/lightProbe/Original/png/equirectangular/03-Ueno-Shrine_3k.jpg';
rgb = im2double(imread(img_path));

% use sphere to define vectors x, y, and z
[X,Y,Z] = sphere(1000);

% compare different implementation
subplot(1, 2, 1);
title('implementation');
texture_mapping(rgb, X, Y, Z);
subplot(1, 2, 2);
title('matlab api');
texture_mapping_api(rgb, X, Y, Z);

%% texture_mapping
% Description: this function is used to implement mapping from Cartesian
% coordinates to spherical coordinates and to uv coordinates.
% Reference: 
% @ https://en.wikipedia.org/wiki/Spherical_coordinate_system

% Input:
% @ rgb: equirectangular environmental map
% @ X: Cartesian coordinates x
% @ Y: Cartesian coordinates y
% @ Z: Cartesian coordinates z
% Output:
% @ a visualiation of a colored point cloud

function texture_mapping(rgb, X, Y, Z)
[h,w,~] = size(rgb);
x = X(:); y = Y(:); z = Z(:);

% cartesian coordinates to spherical coordinates
r = sqrt(x.^2+y.^2+z.^2);
phi = atan2(y,x); % (-pi,pi], azimuth
theta = acos(z./r); % [0,pi], inclination

% get uv coordinates
u = phi./(2*pi) + 0.5;
v = theta./pi;

% map uv to pixel scale
m = ceil(u*(w-1))+1;
n = ceil(v*(h-1))+1;

% generate color of point cloud based on pixel scaled uv
r = rgb(:,:,1); g = rgb(:,:,2); b = rgb(:,:,3);
r = r(sub2ind(size(r), n, m));
g = g(sub2ind(size(g), n, m));
b = b(sub2ind(size(b), n, m));
c = [r g b];

% create point cloud
pcshow(pointCloud([X(:),Y(:),Z(:)], 'Color', c));
end

%% texture_mapping_api
% Description: this function is used to implement texture_mapping using
% Matlab API
% Reference: 
% @ https://www.mathworks.com/help/vision/ref/pcshow.html

% Input:
% @ rgb: equirectangular environmental map
% @ X: Cartesian coordinates x
% @ Y: Cartesian coordinates y
% @ Z: Cartesian coordinates z
% Output:
% @ a visualiation of a colored point cloud

function texture_mapping_api(rgb, X, Y, Z)
tex = flipud(imresize(rgb, size(X)));
pcshow([X(:),Y(:),Z(:)], reshape(tex, [], 3));
end