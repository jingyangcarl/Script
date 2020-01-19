%% clear
clear all;

%% load images
depth = double(rgb2gray(imread('D415.01.IR.L.png')));

%% set parameters
focalLenth = 1.88; % mm
baseline = 55; % mm

%% get disparity map using depth value
disparity = (focalLenth * baseline) ./ depth;

%% recalculate depth map using disparity
depth_reconstructed = (focalLenth * baseline) ./ disparity;

%% calculate the difference
diff_disparity_depthReconstructed = disparity - depth_reconstructed;
diff_depth_depthReconstructed = depth - depth_reconstructed;

%% plot
figure(1);
subplot(2, 3, 1);
imshow(rescale(depth));
title('Depth Image');
subplot(2, 3, 2);
imshow(rescale(disparity));
title('Disparity Image');
subplot(2, 3, 3);
imshow(rescale(depth_reconstructed));
title('Reconstructed Depth Image');
subplot(2, 3, 4);
imshow(rescale(diff_disparity_depthReconstructed));
title('Diff on Disparity and Reconstructed Depth');
subplot(2, 3, 5);
imshow(rescale(diff_depth_depthReconstructed));
title('Diff on Depth and Reconstructed Depth');
subplot(2, 3, 6);
histogram(rescale(diff_depth_depthReconstructed));
title('Diff Histogram');