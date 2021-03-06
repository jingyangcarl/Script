%% spherical_texture_mapping.m
% Description: this code is used to map any equirectangular environmental
% map onto a sphere.

% Author: Jing Yang

clear all;
close all;
% img_path = 'D:/data/lightProbe/Original/png/equirectangular/Bunker_04_Ref.jpg';
% img_path = 'D:/data/lightProbe/Original/png/equirectangular/Chelsea_Stairs_3k.jpg';
% img_path = 'D:/data/lightProbe/Original/png/equirectangular/Factory_Catwalk_2k.jpg';
% img_path = 'D:/data/lightProbe/Original/png/equirectangular/GCanyon_C_YumaPoint_3k.jpg';
% img_path = 'D:/data/lightProbe/Original/png/equirectangular/glacier.jpg';
% img_path = 'D:/data/lightProbe/Original/png/equirectangular/Harbour_2_Ref.jpg';

% img_path = 'D:/data/lightProbe/Original/hdr/Bunker_04_Ref.hdr';
% img_path = 'D:/data/lightProbe/Original/hdr/Chelsea_Stairs_3k.hdr'; % too much brigher
% img_path = 'D:/data/lightProbe/Original/hdr/Factory_Catwalk_2k.hdr';
% img_path = 'D:/data/lightProbe/Original/hdr/GCanyon_C_YumaPoint_3k.hdr';
% img_path = 'D:/data/lightProbe/Original/hdr/glacier.hdr';
img_path = 'D:/data/lightProbe/Original/hdr/Harbour_2_Ref.hdr';

% read image based on file type
if contains(img_path, 'hdr')
    rgb = hdrread(img_path);
    gain = 1.0;
    gamma = 1.5;
    rgb = min(gain * (rgb.^gamma), 10);
elseif contains(img_path, 'jpg')
    rgb = im2double(imread(img_path));
end

% compare different implementation
subplot(1, 3, 1);
[X,Y,Z] = pcloud_sphere_init(rgb, 100);
texture_mapping(rgb, X,Y,Z);
title('implementation');
xlabel('X');
ylabel('Y');
zlabel('Z');

subplot(1, 3, 2);
u_rot = -90/360;
texture_mapping_easy(rgb, 100, u_rot);
title('implementation easy');
xlabel('X');
ylabel('Y');
zlabel('Z');

subplot(1, 3, 3);
[X,Y,Z] = pcloud_sphere_init_api(1000);
texture_mapping_api(rgb, X, Y, Z);
title('matlab api');
xlabel('X');
ylabel('Y');
zlabel('Z');

%% pcloud_sphere_init
% Description: this function is used to generate a point cloud in spherical
% shape from the size of texture map, where density of the points is
% controlled by the step
% Reference: 
% @ https://en.wikipedia.org/wiki/Spherical_coordinate_system

% Input:
% @ rgb: equirectangular environmental map
% @ step: step of sampling on rgb map
% Output:
% @ X: Cartesian coordinates x
% @ Y: Cartesian coordinates y
% @ Z: Cartesian coordinates z
function [X, Y, Z] = pcloud_sphere_init(rgb, step)
% get uv coordinates
[h,w,~] = size(rgb);
u = ((1:step:w)/w)';
v = ((1:step:h)/h)';

% get spherical coordinates
r = 1;
phi = (u) * 2*pi;
theta = v * pi;

% spherical coordinates to cartesian coordinates
X = r .* sin(theta) .* cos(phi)';
Y = r .* sin(theta) .* sin(phi)';
Z = r .* cos(theta) .* ones(size(phi))';
end

%% pcloud_sphere_init_api
% Description: this function is used to generate a point cloud in spherical
% shape by indicating the number of points on the sphere

% Input:
% @ num: the number of points on the sphere
% Output:
% @ X: Cartesian coordinates x
% @ Y: Cartesian coordinates y
% @ Z: Cartesian coordinates z
function [X, Y, Z] = pcloud_sphere_init_api(num)
[X, Y, Z] = sphere(num);
end

%% texture_mapping
% Description: this function is used to implement mapping from Cartesian
% coordinates to spherical coordinates and to uv coordinates for color reference.
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
scalar = 5;
pcshow(pointCloud([scalar*x,scalar*y,scalar*z], 'Color', c));

% rendering diffuse light
hold on;
shading(x,y,z, c);
end

%% texture_mapping_easy
% Description: this function is used to implement mapping from a single
% texture image onto a sphere point cloud.

% Input:
% @ rgb: equirectangular environmental map
% @ step: step of sampling on rgb map
% Output:
% @ a visualiation of a colored point cloud
function texture_mapping_easy(rgb, step, u_rot)
% get uv coordinates
[h,w,~] = size(rgb);
u = ((1:step:w)/w)';
v = ((1:step:h)/h)';

% get spherical coordinates
r = 1;
phi = (u+0.5+u_rot) * 2*pi; % (-pi,pi], azimuth
theta = v * pi; % [0,pi], inclination

% spherical coordinates to cartesian coordinates
X = r .* sin(theta) .* cos(phi)';
Y = r .* sin(theta) .* sin(phi)';
Z = r .* cos(theta) .* ones(size(phi))';

% rendering mapped texture
c = rgb(1:step:h, 1:step:w,:);
c_w = repmat(sin(theta), 1,size(c,2)); % sin(((1:step:h)/h)'*pi), used to equalize light distribution
c = reshape(c.*c_w, [], 3);
scalar = 5;
pcshow(pointCloud([scalar*X(:), scalar*Y(:), scalar*Z(:)], 'Color', reshape(c, [], 3)));

% rendering diffuse light
hold on;
shading(X,Y,Z, c);
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
scalar = 5;
pcshow([scalar*X(:),scalar*Y(:),scalar*Z(:)], reshape(tex, [], 3));
end

%% rendering
% Description: this function is used to render a sphere as well as it's
% color based on diffuse rendering equation for direct light

% Input:
% @ X: Cartesian coordinates x
% @ Y: Cartesian coordinates y
% @ Z: Cartesian coordinates z
% @ c: color value corresponding to XYZ
% Output:
% @ a visualiation of a colored point cloud
function shading(X,Y,Z, c)
[x,y,z] = sphere(200);
norm = [x(:),y(:),z(:)];
l_dir = [X(:),Y(:),Z(:)];
l_color = reshape(c, [], 3);
nDotL = max(norm * l_dir', 0);
light_diffuse = 5.0 * (nDotL * l_color) / (size(l_color,1));
pcshow(pointCloud([x(:),y(:),z(:)],'Color', light_diffuse));
end