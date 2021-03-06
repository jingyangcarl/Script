function extrinsic2JSON(f_in_name)

%% 
view_num = 16;

%% read extrinsics
rts_table = readtable(f_in_name, 'Format', '%f%f%f%f%f%f%f', 'FileType', 'text'); % r_w, r_x, r_y, r_z, t_x, t_y, t_z
rts = rts_table{:,:};
rts_color = rts(3:3:end,:);
clear rts_table;

%% fill in JSON obj
json_obj = struct;
json_obj.camera_angle_x = 1.2112585306167603;
json_obj.frames = [];
for i = 1:view_num
    % write rgb frame file_path
    json_obj.frames(i).file_path = sprintf('./train/r_%d', i-1);
    % write rgb frame rotation, which is a unknown parameter
    json_obj.frames(i).rotation = 0.012566370614359171; % rotation here is a arbitrary value
    % write rgb transform matrix
    json_obj.frames(i).transform_matrix = quat2tform(rts_color(i,1:4));
    json_obj.frames(i).transform_matrix(1:3,4) = rts_color(i,end-2:end);
end

%% json encode
json = jsonencode(json_obj);

%% write json file
f_out_name = "transforms_train.json";
f_id = fopen(f_out_name, 'w');
fprintf(f_id, "%s", json);
fclose(f_id);