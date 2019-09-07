
clc;
clear all;
fontSize=20;
varx=0;
foregroundDetector = vision.ForegroundDetector('NumGaussians', 3, ...
                                               'NumTrainingFrames', 50);

videoReader = vision.VideoFileReader('footage.mp4');
for i = 1:150
frame = step(videoReader); % read the next video frame
foreground = step(foregroundDetector, frame);
end

figure; imshow(frame);
title('Video Frame');

figure; imshow(foreground); title('Foreground');

se = strel('square', 3);
filteredForeground = imopen(foreground, se);
%figure; %imshow(filteredForeground); %title('Clean Foreground');

blobAnalysis = vision.BlobAnalysis('BoundingBoxOutputPort', true, ...
                                   'AreaOutputPort', false, 'CentroidOutputPort', false, ...
                                   'MinimumBlobArea', 150);
bbox = step(blobAnalysis, filteredForeground);

result = insertShape(frame, 'Rectangle', bbox, 'Color', 'green');

numCars = size(bbox, 1);
result = insertText(result, [10 10], numCars, 'BoxOpacity', 1, ...
                    'FontSize', 14);

% result = insertShape(result,'rectangle',[100 700 800 200],'LineWidth',5);
%result = insertShape(result,'rectangle',[1700 950 800 200],'LineWidth',5);
%result = insertShape(result,'rectangle',[1300 150 200 600],'LineWidth',5);
%result = insertShape(result,'rectangle',[1050 1070 200 250],'LineWidth',5);
%figure; %imshow(result); %title('Detected Cars');



videoPlayer = vision.VideoPlayer('Name', 'Detected Cars');
videoPlayer.Position(3:4) = [650,400];  % window size: [width, height]
se = strel('square', 3); % morphological filter for noise removal

while ~isDone(videoReader)

frame = step(videoReader); % read the next video frame

% Detect the foreground in the current video frame
foreground = step(foregroundDetector, frame);

% Use morphological opening to remove noise in the foreground
filteredForeground = imopen(foreground, se);

% Detect the connected components with the specified minimum area, and
% compute their bounding boxes
bbox = step(blobAnalysis, filteredForeground);

% Draw bounding boxes around the detected cars
result = insertShape(frame, 'Rectangle', bbox, 'Color', 'green');




% Display the number of cars found in the video frame
numCars = size(bbox, 1);
result = insertText(result, [10 10], numCars, 'BoxOpacity', 1, ...
                    'FontSize', 14);
result = insertShape(result,'rectangle',[50 155 170 60],'LineWidth',5);
result = insertShape(result,'rectangle',[400 200 170 60],'LineWidth',5);
result = insertShape(result,'rectangle',[310 40 45 130],'LineWidth',5);
result = insertShape(result,'rectangle',[245 265 60 65],'LineWidth',5);


%object masking and counting pixels
% Read in a standard MATLAB gray scale demo image.
%folder = fullfile(matlabroot, '\toolbox\images\imdemos');
% Comment out whichever demo image you don not want to use.
baseFileName = result;
temp=result;% Grayscale demo image.
%baseFileName = result; % Color demo image.
%fullFileName = fullfile(folder, baseFileName);
% See if the image exists.
% Read in the image from disk.
%originalImage = imread(fullFileName);
originalImage = result;
% Get the dimensions of the image.  numberOfColorBands should be = 1.
[rows, columns, numberOfColorBands] = size(originalImage);
% Display the original gray scale image.
subplot(3, 3, 1);


%y= originalImage(:,:,1)>165 & originalImage(:,:,1)<185 & originalImage(:,:,2)>165 & originalImage(:,:,2)<185 & originalImage(:,:,3)>165 & originalImage(:,:,3)<185;
%numPixelstotal = sum(y(:))
%position = [30 30];
%box_color = {'red'};
%originalImage = insertText(originalImage,position,numPixelstotal,'FontSize',50,'BoxColor',...
                            % box_color,'BoxOpacity',0.4,'TextColor','white');


imshow(originalImage, []);
% Change imshow to image() if you don't have the Image Processing Toolbox.
title('Original Image', 'FontSize', fontSize);
% Enlarge figure to full screen.
set(gcf, 'Position', get(0,'Screensize'));
set(gcf,'name','Image Analysis Demo','numbertitle','off')
% Initialize parameters for the circle,
% such as it's location and radius.
circleCenterX = 160;
circleCenterY =  200; % square area 0f 500*500
circleRadius = 80;    % big circle radius
% Initialize an image to a logical image of the circle.
circleImage = false(rows, columns);
[x, y] = meshgrid(1:columns, 1:rows);
circleImage((x - circleCenterX).^2 + (y - circleCenterY).^2 <= circleRadius.^2) = true;
% Display it in the upper right plot.
%couter while loop code

subplot(3,3,2);
imshow(circleImage, []);
title('Circle Mask', 'FontSize', fontSize);
set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
drawnow;



% Mask the image with the circle.
if numberOfColorBands == 1
maskedImage = originalImage; % Initialize with the entire image.
maskedImage(~circleImage) = 0; % Zero image outside the circle mask.
else
% Mask the image.
maskedImage = bsxfun(@times, originalImage, cast(circleImage,class(originalImage)));
end

if varx==0
figure;title('maskedImage');
theta = maskedImage;
varx=1;
end
maskedImageTemp = maskedImage .* 255;
%to display the number of pixels on the image
y= maskedImageTemp(:,:,1)>0 & maskedImageTemp(:,:,2)>0 & maskedImageTemp(:,:,3)>0;
numPixelstotal = sum(y(:))
position = [30 30];
box_color = {'yellow'};
maskedImage = insertText(maskedImage,position,numPixelstotal,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
z= maskedImageTemp(:,:,1)>165 & maskedImageTemp(:,:,1)<185 & maskedImageTemp(:,:,2)>165 & maskedImageTemp(:,:,2)<185 & maskedImageTemp(:,:,3)>165 & maskedImageTemp(:,:,3)<185;
numPixels = sum(z(:))
position = [30 60];
box_color = {'red'};
maskedImage = insertText(maskedImage,position,numPixels,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
% Display it in the lower right plot.
subplot(3, 3, 3);
imshow(maskedImage, []);
% Change imshow to image() if you don't have the Image Processing Toolbox.
title('Image masked with the circle.', 'FontSize', fontSize);
% Change imshow to image() if you don't have the Image Processing Toolbox.






%second lane,toplane start

baseFileName = temp; % Grayscale demo image.
originalImage = temp;
[rows, columns, numberOfColorBands] = size(originalImage);
% Display the original gray scale image.
subplot(3, 3, 4);
imshow(originalImage, []);
% Change imshow to image() if you don't have the Image Processing Toolbox.
title('Original Image', 'FontSize', fontSize);
% Enlarge figure to full screen.
set(gcf, 'Position', get(0,'Screensize'));
set(gcf,'name','Image Analysis Demo','numbertitle','off')
% Initialize parameters for the circle,
% such as it's location and radius.
circleCenterX2 = 350;
circleCenterY2 =  100; % square area 0f 500*500
circleRadius2 = 60;    % big circle radius
% Initialize an image to a logical image of the circle.
circleImage = false(rows, columns);
[x, y] = meshgrid(1:columns, 1:rows);
circleImage((x - circleCenterX2).^2 + (y - circleCenterY2).^2 <= circleRadius2.^2) = true;
% Display it in the upper right plot.
%couter while loop code

subplot(3,3,5);
imshow(circleImage, []);
title('Circle Mask', 'FontSize', fontSize);
set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
drawnow;



% Mask the image with the circle.
if numberOfColorBands == 1
maskedImage = originalImage; % Initialize with the entire image.
maskedImage(~circleImage) = 0; % Zero image outside the circle mask.
else
% Mask the image.
maskedImage = bsxfun(@times, originalImage, cast(circleImage,class(originalImage)));
end

maskedImageTemp = maskedImage .* 255;
%to display the number of pixels on the image
y= maskedImageTemp(:,:,1)>0 & maskedImageTemp(:,:,2)>0 & maskedImageTemp(:,:,3)>0;
numPixelstotal = sum(y(:))
position = [30 30];
box_color = {'yellow'};
maskedImage = insertText(maskedImage,position,numPixelstotal,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
z= maskedImageTemp(:,:,1)>165 & maskedImageTemp(:,:,1)<185 & maskedImageTemp(:,:,2)>165 & maskedImageTemp(:,:,2)<185 & maskedImageTemp(:,:,3)>165 & maskedImageTemp(:,:,3)<185;
numPixels = sum(z(:))
position = [30 60];
box_color = {'red'};
maskedImage = insertText(maskedImage,position,numPixels,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
% Display it in the lower right plot.
subplot(3, 3, 6);
imshow(maskedImage, []);





%end of lane 2,right lane



baseFileName = temp; % Grayscale demo image.
originalImage = temp;
[rows, columns, numberOfColorBands] = size(originalImage);
% Display the original gray scale image.
subplot(3, 3, 7);
imshow(originalImage, []);
% Change imshow to image() if you don't have the Image Processing Toolbox.
title('Original Image', 'FontSize', fontSize);
% Enlarge figure to full screen.
set(gcf, 'Position', get(0,'Screensize'));
set(gcf,'name','Image Analysis Demo','numbertitle','off')
% Initialize parameters for the circle,
% such as it's location and radius.
circleCenterX3 = 450;
circleCenterY3 =  200; % square area 0f 500*500
circleRadius3 = 80;    % big circle radius
% Initialize an image to a logical image of the circle.
circleImage = false(rows, columns);
[x, y] = meshgrid(1:columns, 1:rows);
circleImage((x - circleCenterX3).^2 + (y - circleCenterY3).^2 <= circleRadius3.^2) = true;
% Display it in the upper right plot.
%couter while loop code

subplot(3,3,8);
imshow(circleImage, []);
title('Circle Mask', 'FontSize', fontSize);
set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
drawnow;



% Mask the image with the circle.
if numberOfColorBands == 1
maskedImage = originalImage; % Initialize with the entire image.
maskedImage(~circleImage) = 0; % Zero image outside the circle mask.
else
% Mask the image.
maskedImage = bsxfun(@times, originalImage, cast(circleImage,class(originalImage)));
end

maskedImageTemp = maskedImage .* 255;
%to display the number of pixels on the image
y= maskedImageTemp(:,:,1)>0 & maskedImageTemp(:,:,2)>0 & maskedImageTemp(:,:,3)>0;
numPixelstotal = sum(y(:))
position = [30 30];
box_color = {'yellow'};
maskedImage = insertText(maskedImage,position,numPixelstotal,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
z= maskedImageTemp(:,:,1)>165 & maskedImageTemp(:,:,1)<185 & maskedImageTemp(:,:,2)>165 & maskedImageTemp(:,:,2)<185 & maskedImageTemp(:,:,3)>165 & maskedImageTemp(:,:,3)<185;
numPixels = sum(z(:))
position = [30 60];
box_color = {'red'};
maskedImage = insertText(maskedImage,position,numPixels,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
% Display it in the lower right plot.
subplot(3, 3, 9);
imshow(maskedImage, []);
step(videoPlayer, maskedImage);  % display the results
end



release(videoReader); % close the video file     
