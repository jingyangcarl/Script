close all;
clear all;

img_path_source = 'C:\Users\jingy\Downloads\temp\52480650_0034_s_CUCAU1829024_0034_s.png';
img_path_target = 'D:\data\lightstage\20201218_190044_orange_chelsea_stairs\CUCAU1829008_0000.tif';

img_source = imread(img_path_source);
img_target = imread(img_path_target);

size_source = size(img_source);
size_target = size(img_target);

subplot(2,2,1);
imshow(img_source);
title('image source');
subplot(2,2,2);
imshow(img_target);
title('image target')

colorchart_n = 4;
colorchart_source = zeros(colorchart_n,3);
colorchart_target = zeros(colorchart_n,3);

for img_id = 1:2
    % pick up three corresponding colors from color chart
    for color_id = 1:colorchart_n
        
        % trigger color input
        [x,y] = ginput(1);
        col = round(x);
        row = round(y);
        
        % get its neighbors
        cols = reshape(ones(5) * col + [-2 -1 0 1 2], [],1);
        rows = reshape(ones(5) * row + [-2 -1 0 1 2]', [],1);
        
        switch img_id
            case 1
                % get colors from source images
                rgbs = impixel(img_source, cols, rows);
                colorchart_source(color_id,:) = mean(rgbs);
            case 2
                % get colors from target images
                rgbs = impixel(img_target, cols, rows);
                colorchart_target(color_id,:) = mean(rgbs);
        end
    end
end

% colorchart_source should have same color as colorchart_target, so
% colorchart_source * colorizer = colorchart_target, which means
% [n,3] * [3,3] = [n,3]
colorizer = colorchart_source \ colorchart_target;

% map color space from source to target and vice versa
% ps: img_source is uint8 and img_target is uint16
img_source = reshape(img_source,[],3);
img_target = reshape(img_target,[],3);
img_s2t = uint16(reshape(double(img_source) * colorizer, [], size_source(2),3));
img_t2s = uint8(reshape(double(img_target) / colorizer, [], size_target(2),3));

subplot(2,2,3);
imshow(img_s2t);
title('image source to target');
subplot(2,2,4);
imshow(img_t2s);
title('image target to source');