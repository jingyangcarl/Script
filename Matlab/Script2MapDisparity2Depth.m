%% clear
clear all;

%% load images
depth_L = double(rgb2gray(imread('D415.01.IR.L.png')));

%% set parameters
focalLenth = 1.88; % mm
baseline = 55; % mm

%% get disparity map using depth value
disparity_L = (focalLenth * baseline) ./ depth_L;

%% recalculate depth map using disparity
depth_L_reconstruct = rescale((focalLenth * baseline) ./ disparity_L);

%% calculate the difference
diff_disparity_depthReconstruct_L = disparity_L - depth_L_reconstruct;

%% plot
figure(1);
subplot(2, 3, 1);
imshow(rescale(depth_L));
title('Depth Image');
subplot(2, 3, 2);
imshow(rescale(disparity_L));
title('Disparity Image');
subplot(2, 3, 3);
imshow(depth_L_reconstruct);
title('Reconstructed Depth Image');
subplot(2, 3, 4);
imshow(diff_disparity_depthReconstruct_L);
title('Diff on Disparity and Reconstructed Depth');
subplot(2, 3, 5);
imshow(rescale(diff_disparity_depthReconstruct_L));
title('Rescaled Diff');
subplot(2, 3, 6);
histogram(rescale(diff_disparity_depthReconstruct_L).*256);
title('Diff Histogram');