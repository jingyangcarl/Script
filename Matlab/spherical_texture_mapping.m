clear all;

% hdr = hdrread('D:\data\lightProbe\Original\hdr\03-Ueno-Shrine_3k.hdr');
% png = imread('D:\data\lightProbe\Original\png\equirectangular\03-Ueno-Shrine_3k.jpg');
png = im2double(imread('/home/ICT2000/jyang/Documents/Data/ForJing/lightProbe/Original/png/equirectangular/03-Ueno-Shrine_3k.jpg'));

texture_mapping(png, 550);


function texture_mapping(rgb, samples)

[w,h,ch] = size(rgb);

% use sphere to define vectors x, y, and z
[X,Y,Z] = sphere(samples);
xyz = [X(:),Y(:),Z(:)];
x = X(:); y = Y(:); z = Z(:);

% cartesian coordinates to spherical coordinates
% reference: https://en.wikipedia.org/wiki/Spherical_coordinate_system
r = sqrt(x.^2+y.^2+z.^2);
phi = atan2(y,x); % (-pi,pi], azimuth
theta = acos(z./r); % [0,pi], inclination

% get uv coordinates
u = phi./(2*pi) + 0.5;
v = theta./pi;

m = ceil(u*(w-1))+1;
n = ceil(v*(h-1))+1;

% modify color of point cloud
r = rgb(:,:,1); g = rgb(:,:,2); b = rgb(:,:,3);
r = r(sub2ind(size(r), m, n));
g = g(sub2ind(size(g), m, n));
b = b(sub2ind(size(b), m, n));
c = [r g b];

% create point cloud
pcshow(pointCloud(xyz, 'Color', c));
axis equal;

end


function texture_mapping_matlab(rgb, samples)


end