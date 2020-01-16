%% load images
depth_L = rescale(double(imread('D415.IR.L.R(+22.5d).up.png')));

%% set parameters
focalLenth = 1.88; % mm
baseline = 55; % mm

%% get disparity map using depth value
disparity_L = rescale(1.88./(55.*double(L)));

%% recalculate depth map using disparity
depth_L_reconstruct = rescale(1.88./55.*double(disparity_L));

%% calculate the difference
diff_disparity_depthReconstruct_L = rescale(disparity_L - depth_L_reconstruct);
diff_disparity_depth_L = rescale(disparity - depth_L);
diff_depth_depthReconstruct_L = rescale(depth_L - depth_L_reconstruct);

%% plot
figure(1);
subplot(2, 3, 1);
imshow(depth_L);
title('Depth Image');
subplot(2, 3, 2);
imshow(depth_L_reconstruct);
title('Reconstructed Depth Image');
subplot(2, 3, 3);
imshow(disparity_L);
title('Disparity Image');
subplot(2, 3, 4);
imshow(diff_depth_depthRecover_L);
title('Diff on Depth and Reconstructed Depth');
subplot(2, 3, 5);
imshow(diff_disparity_depth_L);
title('Diff on Disparity and Depth');
subplot(2, 3, 6);
imshow(diff_disparity_depthReconstruct_L);
title('Diff on Disparity and Reconstructed Depth');