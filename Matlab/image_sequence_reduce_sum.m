clear all;
close all;

% ffmpeg.exe -i .\dtla_close.mp4 dtla_close\file%03d.bmp

folder_path = 'D:/data/dji/20201231/';
scene_name = 'marina';
start = 1;
step = 1;
range = 30;

img_sum = zeros();
for i = start:start+range
    img_name = strcat(scene_name, sprintf('/file%03d.bmp', i));
    img_path = strcat(folder_path, img_name);
    img = double(imread(img_path));
    img_sum = img_sum + img;
end

img_reduce_sum = uint8(img_sum / range);
imwrite(img_reduce_sum, strcat(folder_path, scene_name, '_reduce_sum.jpg'));
imshow(img_reduce_sum);

% img_max = zeros();
% for i = start:step:start+range
%     img_name = strcat(scene_name, sprintf('/file%04d.bmp', i));
%     img_path = strcat(folder_path, img_name);
%     img = imread(img_path);
%     img_max = max(img_max, img);
% end
% imwrite(img_max, strcat(folder_path, scene_name, '_max.jpg'));
% imshow(img_max);