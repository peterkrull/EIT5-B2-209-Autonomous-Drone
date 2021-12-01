clear
set(findall(gcf,'-property','FontSize'),'FontSize',13)
set(findall(gcf,'-property','Font'),'Font','Roman')
exportFigures = false;

areaWidth = 2.05; %Width of the flight area
areaHeight = 3.45; %Height of the flight area
courseWidth = .15; %Buffer around route
courseStdHeight = 1; %standard height at which the drone will complete the course
ppRoute = 400; %Points per route segment
startHeight = 0; %Height at which the drone starts and stops its course route
courseScale = 1;

%Matrix definition
%x,y,z,yaw,hold time,checkpoint, ViconAvailable


%Defines the starting point
startPoint = [areaWidth/2 areaHeight/2 courseStdHeight];

%Defines the first set point
firstSetPoint = [startPoint(1)-(areaWidth-courseWidth) startPoint(2) courseStdHeight];
%Generates a number of points from the start point to the first set point
courseToFirstSetPoint = [linspace(startPoint(1),firstSetPoint(1),ppRoute); linspace(startPoint(2),firstSetPoint(2),ppRoute);linspace(startPoint(3),firstSetPoint(3),ppRoute)]';
%Yaw description
yaw1 = 270*ones(ppRoute,1);
%Adds checkpoints
checkPoints = zeros(ppRoute,1);
checkPoints(1) = 1;
checkPoints(ppRoute) = 1;
%StationKeeping [s]
holdTime = zeros(ppRoute,1);
holdTime(1) = 10;
%Vicon available
vicon = ones(ppRoute,1);
%Adds the first part of the course to the total course
totalCourse = [courseToFirstSetPoint yaw1 holdTime checkPoints vicon];

%Defines the second setpoint and generates route from the first to the
%second set point
secondSetPoint = [firstSetPoint(1) firstSetPoint(2)-1 courseStdHeight];
courseToSecondSetPoint = [linspace(firstSetPoint(1),secondSetPoint(1),ppRoute); linspace(firstSetPoint(2),secondSetPoint(2),ppRoute);linspace(firstSetPoint(3),secondSetPoint(3),ppRoute)]';
yaw2 = (yaw1(1)-90)*ones(ppRoute,1);
checkPoints = zeros(ppRoute,1);
checkPoints(1) = 0;
checkPoints(ppRoute) = 1;
holdTime = zeros(ppRoute,1);
totalCourse = [totalCourse; courseToSecondSetPoint yaw2 holdTime checkPoints vicon];

%Defines the first curve in the route, radius is .5 meters
obstacleRadius = .5;
thirdSetPoint = [secondSetPoint(1) secondSetPoint(2)-2*obstacleRadius courseStdHeight];
thirdSetPointPoints = linspace(0,pi,ppRoute);
courseToThirdSetPoint = [secondSetPoint(1)+sin(thirdSetPointPoints)*obstacleRadius; secondSetPoint(2)-obstacleRadius+cos(thirdSetPointPoints)*obstacleRadius; linspace(secondSetPoint(3),thirdSetPoint(3),length(thirdSetPointPoints))]';
yaw3 = yaw2;
totalCourse = [totalCourse; courseToThirdSetPoint yaw3 holdTime checkPoints vicon];

%Generates straight line from the first curve to the second curve
fourthSetPoint = [thirdSetPoint(1) thirdSetPoint(2)-.5 courseStdHeight];
courseToFourthSetPoint = [linspace(thirdSetPoint(1),fourthSetPoint(1),ppRoute); linspace(thirdSetPoint(2),fourthSetPoint(2),ppRoute);linspace(thirdSetPoint(3),fourthSetPoint(3),ppRoute)]';
yaw4 = yaw2;
totalCourse = [totalCourse; courseToFourthSetPoint yaw4 holdTime checkPoints vicon];

%Generates the big curve in the route
bigCurveRadius = abs((fourthSetPoint(1)-startPoint(1))/2);
fifthSetPoint = [fourthSetPoint(1)+2*bigCurveRadius fourthSetPoint(2) courseStdHeight];
fifthSetPointPoints = linspace(pi,2*pi,ppRoute);
courseToFifthSetPoint = [fifthSetPoint(1)-bigCurveRadius+cos(fifthSetPointPoints)*bigCurveRadius; fifthSetPoint(2)+sin(fifthSetPointPoints)*bigCurveRadius; linspace(fourthSetPoint(3),fifthSetPoint(3),length(fifthSetPointPoints))]';
yaw5 = mod(fifthSetPointPoints*180/pi-yaw4(ppRoute),360)';
totalCourse = [totalCourse; courseToFifthSetPoint yaw5 holdTime checkPoints vicon];

%Generates straight movement along the y-axis with oscillation in the
%z-axis
sixthSetPoint = [fifthSetPoint(1) fifthSetPoint(2)+1.5 fifthSetPoint(3)];
pointsForMovements = linspace(0,4*pi,ppRoute);
zMovement = sin(pointsForMovements)*.5+fifthSetPoint(3);
courseToSixthSetPoint = [linspace(fifthSetPoint(1),sixthSetPoint(1),ppRoute);linspace(fifthSetPoint(2),sixthSetPoint(2),ppRoute); zMovement]';
yaw6 = 90*ones(ppRoute,1);
totalCourse = [totalCourse; courseToSixthSetPoint yaw6 holdTime checkPoints vicon];

%Generates route from the end of the oscillations back to the start point
endSetPoint = startPoint;
courseToEndSetPoint = [linspace(sixthSetPoint(1),endSetPoint(1),ppRoute); linspace(sixthSetPoint(2),endSetPoint(2),ppRoute);linspace(sixthSetPoint(3),endSetPoint(3),ppRoute)]';
yaw7 = yaw6;
vicon = zeros(ppRoute,1);
totalCourse = [totalCourse; courseToEndSetPoint yaw7 holdTime checkPoints vicon];


totalCourse = [totalCourse(:,1)*courseScale totalCourse(:,2)*courseScale totalCourse(:,3) totalCourse(:,4) totalCourse(:,5) totalCourse(:,6) totalCourse(:,7)];

%Draws points from start to end 
launchLanding = linspace(startHeight,startPoint(3),ppRoute);
courseToStartPoint = [linspace(startPoint(1)*courseScale,startPoint(1)*courseScale,ppRoute);linspace(startPoint(2)*courseScale,startPoint(2)*courseScale,ppRoute);launchLanding]';


%Draws takeoff/landing zone
aPoints = linspace(0,2*pi,ppRoute);
circumference = [cos(aPoints)*courseWidth+startPoint(1)*courseScale; sin(aPoints)*courseWidth+startPoint(2)*courseScale; ones(1,length(aPoints))*startHeight]';



%Plots the 3d-plot
figure(1)
plot3(totalCourse(:,1),totalCourse(:,2),totalCourse(:,3))
hold on
plot3(courseToStartPoint(:,1),courseToStartPoint(:,2),courseToStartPoint(:,3));
plot3(circumference(:,1),circumference(:,2),circumference(:,3));
%Linie for no vicon data
% Convert color code to 1-by-3 RGB array (0~1 each)
str = '#77AC30';
color = sscanf(str(2:end),'%2x%2x%2x',[1 3])/255;
plot3(totalCourse(2400:end,1),totalCourse(2400:end,2),totalCourse(2400:end,3),'Color',color)
xlimit =[-2.1 0.2];
ylimit =[-3.5 0.05];


%Draws arrow
p1 = [(startPoint(1)-.5)*courseScale (startPoint(2)+.25)*courseScale startPoint(3)];
p2 = [-1 0 0];
mArrow3(p1,p1+p2*courseScale);


legend('Course','Takeoff/Landing','Takeoff/Landing Site','No Vicon data','Location','best');
%legend('boxoff')
hold off

axis equal
grid on
view(-45,15)

x0=0;
y0=0;
plotwidth=600;
height=300;
set(gcf,'position',[x0,y0,plotwidth,height])

if exportFigures == true
    exportgraphics(gcf,'courseToFollow.pdf','ContentType','vector')
end


%Plots the 2d-plot
figure(2)
plot(totalCourse(:,1),totalCourse(:,2))
hold on
plot(circumference(:,1),circumference(:,2))
plot(totalCourse(2400:end,1),totalCourse(2400:end,2),'Color',color)
xlabel('x-axis [m]');
ylabel('y-axis [m]');
zlabel('z-axis [m]');
legend('Course','Takeoff/Landing Site','No Vicon data','Location','south east');
axis equal
grid on
x0=0;
y0=0;
plotwidth=600;
height=300;
set(gcf,'position',[x0,y0,plotwidth,height])
hold off

if exportFigures == true
   exportgraphics(gcf,'courseToFollowAbove.pdf','ContentType','vector')
end

figure(3)
%draws the line segments in different colors
C = {'r'; 'g'; 'b';'c';'m';'y';'k'}; 
plot(totalCourse(1:ppRoute,1),totalCourse(1:ppRoute,2))
hold on 
for i = 2:7
   x = totalCourse((i-1)*ppRoute:ppRoute*i,1);
   y = totalCourse((i-1)*ppRoute:ppRoute*i,2);
   plot(x, y) 
end
hold off
axis equal
legend('line segment 1','line segment 2','line segment 3','line segment 4','line segment 5','line segment 6','line segment 7')
grid on 

xlabel('x-axis [m]');
ylabel('y-axis [m]');
x0=0;
y0=0;
plotwidth=600;
height=300;
set(gcf,'position',[x0,y0,plotwidth,height])

xlim([-1.5 2.5]);
ylim([-1 2]);

%Writes route description to a csv-file
writematrix(totalCourse,'courseDescriptionHD.csv');

figure(4)
plot(linspace(1,length(totalCourse), length(totalCourse)), totalCourse(:,4))
