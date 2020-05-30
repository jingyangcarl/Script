function showCamFromExtrinsic(f_name)
% extrinsics
rts_table = readtable(f_name, 'Format', '%f%f%f%f%f%f%f', 'FileType', 'text'); % r_w, r_x, r_y, r_z, t_x, t_y, t_z
rts = rts_table{:,:};
len = size(rts, 1);
clear rts_table;

%% plot cameras
% the initial position of Blender camera is pointing at negative z axis;
% the initial position of Matlab camera is pointing at positive z axis;
% Blender and Matlab both use the right handed coordination system, 
% which means we have to do y flip before apply the quaternion rotation;
% that is to say, we need to multiply [0.0, 0.0, 1.0, 0.0];
% moreover, the upvector of the two camera system is also flipped,
% which means we have to do z flip as well;

% show cam
for i = 1:len
    t = rts(i,end-2:end);
    
    r = quaternion(rts(i, 1:4)) * quaternion([0.0, 0.0, 1.0, 0.0]) * quaternion([0.0, 0.0, 0.0, 1.0]);
    % r = quaternion(rts(i, 1:4));
    colormap default;
    cmap = colormap;
    
    plotCamera('Label', sprintf('%02d',i), 'Location', t, 'Orientation', quat2rotm(r)', 'Size', 0.05, 'Color', cmap(round(i/len*size(cmap, 1)),:));
    hold on;
end

% configure display
axis equal;
grid on;
xlabel('x');
ylabel('y');
zlabel('z');
colorbar;

end