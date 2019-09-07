clc;
clear all;
fontSize=20;
varx=0;
flag=0;%for writing into the file everytime it's opened
exp1=0;%excption flags for checking skewed traffic conditions
exp2=0;
exp3=0;
EmergencyFlag1=0;
EmergencyFlag2=0;
EmergencyFlag3=0;
globalflag=0;
priorityHistory=[4,5]; %for priority inversion


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
%for manual insertion of Region of Interest.
%result = insertShape(result,'rectangle',[50 155 170 60],'LineWidth',5);
%result = insertShape(result,'rectangle',[400 200 170 60],'LineWidth',5);
%result = insertShape(result,'rectangle',[310 40 45 130],'LineWidth',5);
%result = insertShape(result,'rectangle',[245 265 60 65],'LineWidth',5);


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
%set(gcf, 'Position', get(0,'Screensize'));
%set(gcf,'name','Image Analysis Demo','numbertitle','off')
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
%set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
%drawnow;



% Mask the image with the circle.
if numberOfColorBands == 1
maskedImage1 = originalImage; % Initialize with the entire image.
maskedImage1(~circleImage) = 0; % Zero image outside the circle mask.
else
% Mask the image.
maskedImage1 = bsxfun(@times, originalImage, cast(circleImage,class(originalImage)));
end

if varx==0
%figure;title('maskedImage');
theta = maskedImage1;
varx=1;
end
maskedImageTemp1 = maskedImage1 .* 255;
%to display the number of pixels on the image
y= maskedImageTemp1(:,:,1)>0 & maskedImageTemp1(:,:,2)>0 & maskedImageTemp1(:,:,3)>0;
numPixelstotal = sum(y(:))
position = [30 30];
box_color = {'yellow'};
maskedImage1 = insertText(maskedImage1,position,numPixelstotal,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
z= maskedImageTemp1(:,:,1)>165 & maskedImageTemp1(:,:,1)<185 & maskedImageTemp1(:,:,2)>165 & maskedImageTemp1(:,:,2)<185 & maskedImageTemp1(:,:,3)>165 & maskedImageTemp1(:,:,3)<185;
numPixelsLane1 = sum(z(:))
%for emergency conditions
theta1= ( maskedImageTemp1(:,:,1)<40 ) & maskedImageTemp1(:,:,2)<50 & (maskedImageTemp1(:,:,3)>245);
EmergencyPixels1=sum(theta1(:))
if EmergencyPixels1>100
EmergencyFlag1=1;
end
position = [30 60];
box_color = {'red'};
maskedImage1 = insertText(maskedImage1,position,numPixelsLane1,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
% Display it in the lower right plot.
subplot(3, 3, 3);
imshow(maskedImage1, []);
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
%title('Original Image', 'FontSize', fontSize);
% Enlarge figure to full screen.
%set(gcf, 'Position', get(0,'Screensize'));
%set(gcf,'name','Image Analysis Demo','numbertitle','off')
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
%title('Circle Mask', 'FontSize', fontSize);
%set(gcf, 'Position', get(0,'Screensize')); % Maximize figure.
%drawnow;



% Mask the image with the circle.
if numberOfColorBands == 1
maskedImage2 = originalImage; % Initialize with the entire image.
maskedImage2(~circleImage) = 0; % Zero image outside the circle mask.
else
% Mask the image.
maskedImage2 = bsxfun(@times, originalImage, cast(circleImage,class(originalImage)));
end

maskedImageTemp2 = maskedImage2 .* 255;
%to display the number of pixels on the image
y= maskedImageTemp2(:,:,1)>0 & maskedImageTemp2(:,:,2)>0 & maskedImageTemp2(:,:,3)>0;
numPixelstotal = sum(y(:))
position = [30 30];
box_color = {'yellow'};
maskedImage2 = insertText(maskedImage2,position,numPixelstotal,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
z= maskedImageTemp2(:,:,1)>165 & maskedImageTemp2(:,:,1)<185 & maskedImageTemp2(:,:,2)>165 & maskedImageTemp2(:,:,2)<185 & maskedImageTemp2(:,:,3)>165 & maskedImageTemp2(:,:,3)<185;
numPixelsLane2 = sum(z(:))
theta2= ( maskedImageTemp2(:,:,1)<40 ) & maskedImageTemp2(:,:,2)<50 & (maskedImageTemp2(:,:,3)>245);
EmergencyPixels2=sum(theta2(:))
if EmergencyPixels2>100
EmergencyFlag2=1;
end
position = [30 60];
box_color = {'red'};
maskedImage2 = insertText(maskedImage2,position,numPixelsLane2,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
% Display it in the lower right plot.
subplot(3, 3, 6);
imshow(maskedImage2, []);





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
%set(gcf, 'Position', get(0,'Screensize'));
%set(gcf,'name','Image Analysis Demo','numbertitle','off')
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
maskedImage3 = originalImage; % Initialize with the entire image.
maskedImage3(~circleImage) = 0; % Zero image outside the circle mask.
else
% Mask the image.
maskedImage3 = bsxfun(@times, originalImage, cast(circleImage,class(originalImage)));
end

maskedImageTemp3 = maskedImage3 .* 255;
%to display the number of pixels on the image
y= maskedImageTemp3(:,:,1)>0 & maskedImageTemp3(:,:,2)>0 & maskedImageTemp3(:,:,3)>0;
numPixelstotal = sum(y(:))
position = [30 30];
box_color = {'yellow'};
maskedImage3 = insertText(maskedImage3,position,numPixelstotal,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
z= maskedImageTemp3(:,:,1)>165 & maskedImageTemp3(:,:,1)<185 & maskedImageTemp3(:,:,2)>165 & maskedImageTemp3(:,:,2)<185 & maskedImageTemp3(:,:,3)>165 & maskedImageTemp3(:,:,3)<185;
numPixelsLane3 = sum(z(:))
theta3= ( maskedImageTemp3(:,:,1)<40 ) & maskedImageTemp3(:,:,2)<50 & (maskedImageTemp3(:,:,3)>245);
EmergencyPixels3=sum(theta3(:))
if EmergencyPixels3>100
EmergencyFlag3=1;
end
position = [30 60];
box_color = {'red'};
maskedImage3 = insertText(maskedImage3,position,numPixelsLane3,'FontSize',20,'BoxColor',box_color,'BoxOpacity',0.4,'TextColor','white');
% Display it in the lower right plot.
subplot(3, 3, 9);
imshow(maskedImage3, []);
step(videoPlayer, maskedImage3);  % display the results

arr=[numPixelsLane1,numPixelsLane2,numPixelsLane3];
sortedArr = arr;

if flag==0
    fileID = fopen('schedulingNew.txt','w');
    flag=1;
else
    fileID=fopen('schedulingNew.txt','a');
end
%scheduling algorithm
s1=numPixelsLane1;
s2=numPixelsLane2;
s3=numPixelsLane3;

           if s2>s1
            if s3>s2
                max=s3;
                mid=s2;
                min=s1;
                p1=1;   %for setting the priorities of teach signal according to the traffic density
                p2=2;
                p3=3;
            
            else
            if s1>s3
                max=s2;
                mid=s1;
                min=s3;
                p1=3;   %for setting the priorities of teach signal according to the traffic density
                p2=1;
                p3=2;
  
            else
                max=s2;
                mid=s3;
                min=s1;
                p1=1;   %for setting the priorities of teach signal according to the traffic density
                p2=3;
                p3=2;
                
                end
            end
         else
            if s3>s1
                max=s3;
                mid=s1;
                min=s2;
                p1=2;   %for setting the priorities of teach signal according to the traffic density
                p2=1;
                p3=3;
            
            else
                if s2>s3
                max=s1;
                mid=s2;
                min=s3;
                p1=3;   %for setting the priorities of teach signal according to the traffic density
                p2=2;
                p3=1;
 
                else
                max=s1;
                mid=s3;
                min=s2;
                p1=2;  %for setting the priorities of teach signal according to the traffic density
                p2=3;
                p3=1;
                
  
                end
            end
           end
          

        %get the ratio of the signal allotment and assuming that next signal read is done before 2mins 120000 MilSec
        totalRatio=s1+s2+s3;
        minTime=min*(120/totalRatio);
        maxTime=max*(120/totalRatio);
        midTime=mid*(120/totalRatio);
        %s1=120-(s1*(120/totalRatio));
        %s2=120-(s2*(120/totalRatio));
        %s3=120-(s3*(120/totalRatio));
        
        %by now we know how much time should be allocated to each side of the signal
        %now we need to give each signal the time which should be allocated according to p1 p2 p3
        r1=s1/max;  %ratios for
        r2=s2/max;
        r3=s3/max;
        
        %saving the priority allocated
        priorityHistory= [priorityHistory,p1];
        plength=length(priorityHistory);
   %check for emergency conditions
          
       if EmergencyFlag1==1 & EmergencyFlag2==0 & EmergencyFlag3==0
      %then signal s1
                    % Start a timer: 
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while EmergencyPixels1~=0
                       fprintf(fileID,'%d,',3);
                       pause(0.1);
                       theta1= ( maskedImageTemp1(:,:,1)<40 ) & maskedImageTemp1(:,:,2)<50 & (maskedImageTemp1(:,:,3)>245);
                       EmergencyPixels1=sum(theta1(:))
                    end
       elseif EmergencyFlag1==0 & EmergencyFlag2==1 & EmergencyFlag3==0
      %then signal s2
                    % Start a timer: 
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while EmergencyPixels2~=0
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
                       theta2= ( maskedImageTemp2(:,:,1)<40 ) & maskedImageTemp2(:,:,2)<50 & (maskedImageTemp2(:,:,3)>245);
                       EmergencyPixels2=sum(theta2(:))
                    end
       elseif EmergencyFlag1==0 & EmergencyFlag2==0 & EmergencyFlag3==1
      %then signal s1
                    % Start a timer: 
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while EmergencyPixels3~=0
                       fprintf(fileID,'%d,',9);
                       pause(0.1);
                       theta3= ( maskedImageTemp3(:,:,1)<40 ) & maskedImageTemp3(:,:,2)<50 & (maskedImageTemp3(:,:,3)>245);
                       EmergencyPixels3=sum(theta3(:))
                    end
       else
        if p1==1
            
            if r2<0.001 && r3<0.001 %checking for skewed conditions
                if r2<r3
                    %raise the exception flags to avoid signaling again
                    exp2=1;
                    exp3=1;
                    
                        tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',int(6));
                       pause(0.1);
                    end
                          tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',int(9));
                       pause(0.1);
                    end
                else
                         tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',int(9));
                       pause(0.1);
                    end
                      tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',int(6));
                       pause(0.1);
                    end
                end
            
            
        elseif r2<0.001
            exp2=1;
                % Start a timer: 
            tic       
            % Do this loop over and over until the timer reaches RunFor seconds:  
            while toc<s2 
               fprintf(fileID,'%d,',int(6));
               pause(0.1);
            end
            
        elseif r3<0.001
            exp3=1;
                % Start a timer: 
            tic       
            % Do this loop over and over until the timer reaches RunFor seconds:  
            while toc<s3 
               fprintf(fileID,'%d,',int(9));
               pause(0.1);
            end
            s1=maxTime;
            end  
        
            %if traffic is not skewed hence signal according to the
            %scheduling time
            if priorityHistory(plength)~=priorityHistory(plength-1) && priorityHistory(plength-2)~=priorityHistory(plength-1) &&priorityHistory(plength)==1
                % Start a timer: 
                tic       
                % Do this loop over and over until the timer reaches RunFor seconds:  
                while toc<(s1-10) 
                   fprintf(fileID,'%d,',int(3));
                   pause(0.1);
                end
            else
                              % Start a timer: 
                tic       
                % Do this loop over and over until the timer reaches RunFor seconds:  
                while toc<(s1-10) 
                   fprintf(fileID,'%d,',int(3));
                   pause(0.1);
                end  
            end
            
            %after p1
            
            if p2==2
                if exp2==0
                    s2=midTime;
                        % Start a timer: 
                        tic       
                        % Do this loop over and over until the timer reaches RunFor seconds:  
                        while toc<s2 
                           fprintf(fileID,'%d,',int(6));
                           pause(0.1);
                        end
                    end
                if exp3==0
                    %then signal3
                    % Start a timer: 
                    s3=minTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',int(9));
                       pause(0.1);
                    end
                end
            
            else
                if exp3==0
                    % Start a timer:
                    s3=midTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',9);
                       pause(0.1);
                    end
                end
                if exp2==0
                    %then signal s2
                    % Start a timer:
                    s2=minTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
                    end
                end
            end
        end

       
            
        
        
        if p1==2
             if r1<0.001 && r3<0.001 %checking for skewed conditions
                if r1<r3
                    %raise the exception flags to avoid signaling again
                    exp1=1;
                    exp3=1;
                    
                        tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',int(3));
                       pause(0.1);
                    end
                          tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',int(9));
                       pause(0.1);
                    end
                else
                         tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',int(9));
                       pause(0.1);
                    end
                      tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',int(3));
                       pause(0.1);
                    end
                end
            
            
        elseif r1<0.001
            exp1=1;
                % Start a timer: 
            tic       
            % Do this loop over and over until the timer reaches RunFor seconds:  
            while toc<s1 
               fprintf(fileID,'%d,',int(3));
               pause(0.1);
            end
            
        elseif r3<0.001
            exp3=1;
                % Start a timer: 
            tic       
            % Do this loop over and over until the timer reaches RunFor seconds:  
            while toc<s3 
               fprintf(fileID,'%d,',int(9));
               pause(0.1);
            end
            s1=maxTime;
             end
            %if traffic is not skewed
            
            s2=maxTime;
            if priorityHistory(plength)~=priorityHistory(plength-1) && priorityHistory(plength-2)~=priorityHistory(plength-1) &&priorityHistory(plength)==2            
                % Start a timer: 
                tic       
                % Do this loop over and over until the timer reaches RunFor seconds:  
                while toc<s2 
                   fprintf(fileID,'%d,',6);
                   pause(0.1);
                end
            else
                                  % Start a timer: 
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<(s2-10) 
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
             end 
            end
            %after p2
                if p2==1
                    if exp1==0
                        s1=midTime;
                        % Start a timer: 
                        tic       
                        % Do this loop over and over until the timer reaches RunFor seconds:  
                        while toc<s1 
                           fprintf(fileID,'%d,',3);
                           pause(0.1);
                        end
                    end
            if exp3==0
                %then signal3
                % Start a timer:
                s3=minTime;
                tic       
                % Do this loop over and over until the timer reaches RunFor seconds:  
                while toc<s3 
                   fprintf(fileID,'%d,',9);
                   pause(0.1);
                end
            end
                else
                if exp3==0
                    % Start a timer:
                    s3=midTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s3 
                       fprintf(fileID,'%d,',9);
                       pause(0.1);
                    end
                end
                if exp1==0
                    %then signal s1
                    % Start a timer: 
                    s1=minTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',3);
                       pause(0.1);
                    end
                end        
            end
        end
        
    
        if p1==3
             if r1<0.001 && r2<0.001 %checking for skewed conditions
                if r1<r2
                    %raise the exception flags to avoid signaling again
                    exp1=1;
                    exp2=1;
                    
                        tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',3);
                       pause(0.1);
                    end
                          tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
                    end
                else
                         tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
                    end
                      tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',3);
                       pause(0.1);
                    end
                end
            
            
        elseif r1<0.001
            exp1=1;
                % Start a timer: 
            tic       
            % Do this loop over and over until the timer reaches RunFor seconds:  
            while toc<s1 
               fprintf(fileID,'%d,',3);
               pause(0.1);
            end
            
        elseif r2<0.001
            exp2=1;
                % Start a timer: 
            tic       
            % Do this loop over and over until the timer reaches RunFor seconds:  
            while toc<s2 
               fprintf(fileID,'%d,',6);
               pause(0.1);
            end
            s1=maxTime;
             end
            %if traffic is not skewed            
            
            s3=maxTime;
            if priorityHistory(plength)~=priorityHistory(plength-1) && priorityHistory(plength-2)~=priorityHistory(plength-1) &&priorityHistory(plength)==3            
                % Start a timer: 
                tic       
                % Do this loop over and over until the timer reaches RunFor seconds:  
                while toc<s3 
                   fprintf(fileID,'%d,',9);
                   pause(0.1);
                end
            else
                              % Start a timer: 
                tic       
                % Do this loop over and over until the timer reaches RunFor seconds:  
                while toc<(s3-10) 
                   fprintf(fileID,'%d,',9);
                   pause(0.1);
                end                 
            end
            %after p3
            
            if p2==2
                if exp2==0
                % Start a timer: 
                    s2=midTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
                    end
                end
                if exp1==0
                    %then signal1
                    % Start a timer:
                    s1=minTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',3);
                       pause(0.1);
                    end
                end
            else
                if exp1==0
                    % Start a timer: 
                    s1=midTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s1 
                       fprintf(fileID,'%d,',3);
                       pause(0.1);
                    end
                end
                if exp2==0
                    %then signal s2
                    % Start a timer: 
                    s2=minTime;
                    tic       
                    % Do this loop over and over until the timer reaches RunFor seconds:  
                    while toc<s2 
                       fprintf(fileID,'%d,',6);
                       pause(0.1);
                    end
                end
            end 
        end
        
                   
      end
      
      
%fprintf(fileID,'%f %f %f',0,3,9);
fclose(fileID);
end

release(videoReader); % close the video file   