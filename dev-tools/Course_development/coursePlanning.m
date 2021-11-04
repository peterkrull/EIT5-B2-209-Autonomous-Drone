courseHD = readmatrix('courseDescriptionHD.csv');

pfRadius = .1; %Radius of the pathfollowing algorithme in meters

newCourse = courseHD(1,:);
numOfCoor = 1;

for i = 2:length(courseHD)
   vec = newCourse(numOfCoor,:)-courseHD(i,:);
   
   if pfRadius < norm(vec)
       numOfCoor = numOfCoor +1;
       newCourse = [newCourse;courseHD(i,:)];
   end
    
end

%plot3(courseHD(:,1),courseHD(:,2),courseHD(:,3),'x')
plot3(newCourse(:,1),newCourse(:,2),newCourse(:,3),'o')
grid on
axis equal
yaw = zeros(length(newCourse),1);

newCourse = [newCourse yaw];

toAdd = [newCourse(numOfCoor,1) newCourse(numOfCoor,2) .2 0];
%newCourse = [newCourse; toAdd]*750;
newCourse(:,1) = newCourse(:,1)*750;
newCourse(:,2) = newCourse(:,2)*750+400;
newCourse(:,3) = newCourse(:,3)*1000+300;
writematrix(newCourse,'courseToFollow.csv')