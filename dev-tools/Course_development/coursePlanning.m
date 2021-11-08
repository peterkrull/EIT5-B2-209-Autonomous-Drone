courseHD = readmatrix('courseDescriptionHD.csv');

%Does not work with yaw currently, wip

pfRadius = .2; %Radius of the pathfollowing algorithme in meters

newCourse = courseHD(1,:);
numOfCoor = 1;



for i = 2:length(courseHD)
   vec = newCourse(numOfCoor,1:3)-courseHD(i,1:3);
   
   if pfRadius < norm(vec) | courseHD(i,5) == 1
       numOfCoor = numOfCoor +1;
       newCourse = [newCourse;courseHD(i,:)];
       if newCourse(numOfCoor,4) ~= newCourse(numOfCoor-1,4)
           vec1 = newCourse(numOfCoor,1:2) - newCourse(numOfCoor-1,1:2);
           angle = atan2(vec1(2),vec1(1))*180/pi;
           if angle < 0
              angle = angle +360;
           end
           newCourse(numOfCoor,4) = angle;
       end
   end
    
end

%plot3(courseHD(:,1),courseHD(:,2),courseHD(:,3),'x')
plot3(newCourse(:,1),newCourse(:,2),newCourse(:,3),'o')
grid on
axis equal
%yaw = zeros(length(newCourse),1);

%newCourse = [newCourse yaw];

%Adds checkpoint before landing

toAdd = [newCourse(numOfCoor,1) newCourse(numOfCoor,2) .2 newCourse(numOfCoor,4) 1];
newCourse = [newCourse; toAdd];
newCourse = [newCourse(:,1) newCourse(:,2) newCourse(:,3) newCourse(:,4)];

%Corrects distances to mm
newCourse(:,1) = newCourse(:,1)*1000;
newCourse(:,2) = newCourse(:,2)*1000;
newCourse(:,3) = newCourse(:,3)*1000;
writematrix(newCourse,'courseToFollow.csv')
writematrix([newCourse(:,1) newCourse(:,2) newCourse(:,3)],'courseToFollowNoYaw.csv')