row=360;  col=640;
fin=fopen('xinlei_Depth.raw','r');
I = fread(fin, row*col, 'ubit16=>double');
Z=reshape(I,col,row);
Z=Z';
imshow(Z)