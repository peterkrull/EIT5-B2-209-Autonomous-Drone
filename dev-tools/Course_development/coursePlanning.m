clear
courseHD = readmatrix('courseDescriptionHD.csv');

xColumn = 1;         outputX = true;    printX          = true;
yColumn = 2;         outputY = true;    printY          = true;
zColumn = 3;         outputZ = true;    printZ          = true;
yawColumn = 4;       outputYaw = true;  printYaw        = true;
holdTimeColumn = 5;  outputHT = true;   printHoldTime   = true;
checkpointColumn = 6;outputCP = false;  printCheckPoint = false;
viconColumn = 7;     outputVC = true;   printVicon      = true;

printMatrix = [xColumn outputX printX];
printMatrix = [printMatrix; yColumn outputY printY];
printMatrix = [printMatrix; zColumn outputZ printZ];
printMatrix = [printMatrix; yawColumn outputYaw printYaw];
printMatrix = [printMatrix; holdTimeColumn outputHT printHoldTime];
printMatrix = [printMatrix; checkpointColumn outputCP printCheckPoint];
printMatrix = [printMatrix; viconColumn outputVC printVicon];

pfRadius = .525; %Radius of the pathfollowing algorithme in meters

newCourse = courseHD(1,:);
numOfCoor = 1;



for i = 2:length(courseHD)
   vec = newCourse(numOfCoor,1:3)-courseHD(i,1:3);
   
   if pfRadius < norm(vec) | courseHD(i,6) == 1
       numOfCoor = numOfCoor +1;
       newCourse = [newCourse;courseHD(i,:)]
       if newCourse(numOfCoor,4) ~= newCourse(numOfCoor-1,4)
           vec1 = newCourse(numOfCoor,1:2) - newCourse(numOfCoor-1,1:2)
           angle = atan(vec1(2)/vec1(1))*180/pi
           
           newyaw = newCourse(numOfCoor-1,4) -angle
           if newyaw >=360
               newyaw = newyaw-360
          
           elseif newyaw <0
               newyaw = newyaw +360    
           end
           
           newCourse(numOfCoor,4) = newyaw
           
       end
   end
    
end

%plot3(courseHD(:,1),courseHD(:,2),courseHD(:,3),'x')
plot3(newCourse(:,1),newCourse(:,2),newCourse(:,3),'o')
hold on
grid on
axis equal
plot3(courseHD(:,1),courseHD(:,2),courseHD(:,3))
hold off


%Adds checkpoint before landing

toAdd = [newCourse(numOfCoor,1) newCourse(numOfCoor,2) .2 newCourse(numOfCoor,4) 0 1 1];
newCourse = [newCourse; toAdd];
newCourse = [newCourse(:,1) newCourse(:,2) newCourse(:,3) newCourse(:,4) newCourse(:,5) newCourse(:,6) newCourse(:,7)];

%Corrects distances to mm
newCourse(:,1) = newCourse(:,1)*1000;
newCourse(:,2) = newCourse(:,2)*1000;
newCourse(:,3) = newCourse(:,3)*1000;

%Truncates numbers to 2 decimal places
for i = 1:size(newCourse,1)
   for j = 1:size(newCourse,2)
      newCourse(i,j) = fix(newCourse(i,j)*100)/100;  
   end
end


%Sets columns not chosen to be output to 0
toOutput(:,1) = newCourse(:,1);
for i = 2:size(printMatrix,1)
    if printMatrix(i,2) == true
        if printMatrix(i,3) == true 
            toOutput = [toOutput newCourse(:,i)]; 
        else
            toOutput = [toOutput zeros(i,1)]; 
        end
   end
end

writematrix(toOutput,'courseToFollow.csv')
figure(2)
plot(linspace(1,length(toOutput),length(toOutput)),toOutput(:,4))