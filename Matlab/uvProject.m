close all; clear all;

im =imread('D:\data\yajie\rendered\rp_cornell_rigged_003\Baseball Pitching\0033\17.png');
mesh = ReadMesh('D:\data\yajie\ForZeng\Zeng_Renderpeople_Mixamo\OBJ\rp_cornell_rigged_003\Baseball Pitching\0033.obj');

% from yajie
% R=rt(1:3,1:3);
% t= rt(1:3,4);
% inv_R=inv(R);
% inv_R(1,:) = - inv_R(1,:);
% proj=[inv_R -inv_R*t];

K = [933.0127239227295,   0.0000, 250.0000
0.0000, 933.0127239227295, 250.0000
0.0000,   0.0000,  1.0000];
scale =170;

% mesh rescale
mesh{1} =mesh{1}/(scale);

% get bounding box center
object_max = max(mesh{1});
object_min = min(mesh{1});
object_center = (object_max + object_min) / 2;

% rotate mesh, since blender automatically apply a x-90d rotation
matrix = [1.0000000,  0.0000000,  0.0000000;
   0.0000000,  0.0000000, -1.0000000;
   0.0000000,  1.0000000,  0.0000000 ];
mesh{1} = (matrix * mesh{1}')';

% move mesh to center
object_center_ = (matrix * object_center')';
mesh{1} = mesh{1} - repmat(object_center_, [length(mesh{1}) 1]);

% extrinsic
%vec = [0.7071 0.7071 0.0000 0.0000 0.0000 -2.7320 0.0000]; % view #10
%vec = [0.0000 -0.0000 0.7071 0.7071 -0.0000 2.7320 0.0000]; % view #14
%vec = [0.3536 0.3536 0.6124 0.6124 2.3660 1.3660 0.0000]; % view #15
%vec = [0.6830 0.1830 0.1830 0.6830 1.3660 0.0000 2.3660]; % view #16
vec = [0.8365 0.2241 0.1294 0.4830 1.1830 -0.6830 2.3660]; % view #17
r = vec(1:4);
t = vec(5:7);

% get rt
% the initial position of Blender camera is pointing at negative z axis;
% the initial position of Matlab camera is pointing at positive z axis;
% Blender and Matlab both use the right handed coordination system, 
% which means we have to do y flip before apply the quaternion rotation;
% that is to say, we need to multiply [0.0, 0.0, 1.0, 0.0];
% moreover, the upvector of the two camera system is also flipped,
% which means we have to do z flip as well;
inv_r = quat2rotm(quaternion(r) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]))';
proj = [inv_r -inv_r*t']; % from yajie

% get uv
uv=Project3DPoints(mesh{1},K*proj);
figure(1);imshow(im);hold on;plot(uv(:,1),uv(:,2),'.r');