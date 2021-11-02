xclear
set(findall(gcf,'-property','FontSize'),'FontSize',13)
set(findall(gcf,'-property','Font'),'Font','Roman')


areaWidth = 2.05;
areaHeight = 3.45;
courseWidth = .15;

startPoint = [areaWidth/2 areaHeight/2 1];

firstSetPoint = [startPoint(1)-(areaWidth-courseWidth) startPoint(2) 1];
courseToFirstSetPoint = [linspace(startPoint(1),firstSetPoint(1),100); linspace(startPoint(2),firstSetPoint(2),100);linspace(startPoint(3),firstSetPoint(3),100)]';
totalCourse = [courseToFirstSetPoint];

secondSetPoint = [firstSetPoint(1) firstSetPoint(2)-1 1];
courseToSecondSetPoint = [linspace(firstSetPoint(1),secondSetPoint(1),100); linspace(firstSetPoint(2),secondSetPoint(2),100);linspace(firstSetPoint(3),secondSetPoint(3),100)]';
totalCourse = [totalCourse; courseToSecondSetPoint];

obstacleRadius = .5;
thirdSetPoint = [secondSetPoint(1) secondSetPoint(2)-2*obstacleRadius 1];
thirdSetPointPoints = linspace(0,pi,100);
courseToThirdSetPoint = [secondSetPoint(1)+sin(thirdSetPointPoints)*obstacleRadius; secondSetPoint(2)-obstacleRadius+cos(thirdSetPointPoints)*obstacleRadius; linspace(secondSetPoint(3),thirdSetPoint(3),length(thirdSetPointPoints))]';
totalCourse = [totalCourse; courseToThirdSetPoint];

fourthSetPoint = [thirdSetPoint(1) thirdSetPoint(2)-.5 1];
courseToFourthSetPoint = [linspace(thirdSetPoint(1),fourthSetPoint(1),100); linspace(thirdSetPoint(2),fourthSetPoint(2),100);linspace(thirdSetPoint(3),fourthSetPoint(3),100)]';
totalCourse = [totalCourse; courseToFourthSetPoint];

bigCurveRadius = abs((fourthSetPoint(1)-startPoint(1))/2);
fifthSetPoint = [fourthSetPoint(1)+2*bigCurveRadius fourthSetPoint(2) 1];
fifthSetPointPoints = linspace(pi,2*pi,100);
courseToFifthSetPoint = [fifthSetPoint(1)-bigCurveRadius+cos(fifthSetPointPoints)*bigCurveRadius; fifthSetPoint(2)+sin(fifthSetPointPoints)*bigCurveRadius; linspace(fourthSetPoint(3),fifthSetPoint(3),length(fifthSetPointPoints))]';
totalCourse = [totalCourse; courseToFifthSetPoint];

sixthSetPoint = [fifthSetPoint(1) fifthSetPoint(2)+1.5 fifthSetPoint(3)];
pointsForMovements = linspace(0,4*pi,100);
zMovement = sin(pointsForMovements)*.5+fifthSetPoint(3);
courseToSixthSetPoint = [linspace(fifthSetPoint(1),sixthSetPoint(1),100);linspace(fifthSetPoint(2),sixthSetPoint(2),100); zMovement]';
totalCourse = [totalCourse; courseToSixthSetPoint];


endSetPoint = startPoint;
courseToEndSetPoint = [linspace(sixthSetPoint(1),endSetPoint(1),100); linspace(sixthSetPoint(2),endSetPoint(2),100);linspace(sixthSetPoint(3),endSetPoint(3),100)]';
totalCourse = [totalCourse; courseToEndSetPoint];

launchLanding = linspace(0,startPoint(3),100);
courseToStartPoint = [linspace(startPoint(1),startPoint(1),100);linspace(startPoint(2),startPoint(2),100);launchLanding]';




figure(1)
plot3(totalCourse(:,1),totalCourse(:,2),totalCourse(:,3))
hold on
plot3(courseToStartPoint(:,1),courseToStartPoint(:,2),courseToStartPoint(:,3));

xlabel('x-axis [m]');
ylabel('y-axis [m]');
zlabel('z-axis [m]');
xlimit =[-2.1 0.2];
ylimit =[-3.5 0.05];


%Draws arrow
p1 = [startPoint(1)-.5 startPoint(2)+.25 startPoint(3)];
p2 = [-1 0 0];
quiver3(p1(1),p1(2),p1(3),p2(1),p2(2),p2(3),'LineWidth',1);
legend('Course','Launch/Landing','Location','best');
hold off

grid on


x0=0;
y0=0;
plotwidth=600;
height=300;
set(gcf,'position',[x0,y0,plotwidth,height])
   
