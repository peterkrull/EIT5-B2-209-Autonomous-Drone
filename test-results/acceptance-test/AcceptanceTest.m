clear

Track=readmatrix('APathUHD');
Track= Track(:,1:4);     %Reduce matrix a to needed values RAM OPT
Track(:,1:3) = Track(:,1:3)/1000;   %Calculate in meters

for n=1:length(Track(:,4))
    if Track(n,4) > 180
        Track(n,4) = Track(n,4)-360;
    end 
    Track(n,4) = Track(n,4)*(-1);
end

%Flight=readtable('1638353769_accept_test_dec_1_test1');
%Flight=readtable('1638780111_accept_test_FINAL_v1');
%Flight=readtable('1638780396_accept_test_FINAL_v2');
%Flight=readtable('1638780486_accept_test_FINAL_v3');
Flight=readtable('1638780560_accept_test_FINAL_v4');
%Flight=readtable('1638780701_accept_test_FINAL_v5');


Flight.x_pos = Flight.x_pos/1000; %Calculate in meter
Flight.y_pos = Flight.y_pos/1000;
Flight.z_pos = Flight.z_pos/1000;
Flight.z_rot = Flight.z_rot*180/pi;

disp("Hallow World")

%% Plotting distance to Track
[NearestPointTrack, dist] = dsearchn(Track(:,1:3),[Flight.x_pos Flight.y_pos Flight.z_pos]); %Finding the distance and the pointer to the nearest point on track

figure(1)
plot(Flight.time(:,1), dist,'.')
grid on
xlabel("Time [s]")
ylabel("Distance to closest point on track [m]")
yticks([0.15 0.3 0.45 0.6])
ylim([0 0.7])

x0=0;
y0=0;
plotwidth=500;
height=400;
set(gcf,'position',[x0,y0,plotwidth,height])
exportgraphics(gcf,'TrackDistanceplot4.pdf','ContentType','image')

%% Plotting track
figure(2)

%Gerneration point for time stamp
numberOfTimeStamps = 15;
stepSize = floor( length(Flight.time) /numberOfTimeStamps);
for n=1:numberOfTimeStamps
   stamp(n) = stepSize*n; 
end

    
plot3(Track(:,1),Track(:,2),Track(:,3),Flight.x_pos, Flight.y_pos, Flight.z_pos)
txt = [num2str(round(Flight.time(stamp),1))];   %txt for time stamp
text(Flight.x_pos(stamp), Flight.y_pos(stamp), Flight.z_pos(stamp),txt) %Time stamp
grid on
xlabel("x position [m]")
ylabel("y position [m]")
zlabel("z position [m]")
legend("Track" , "Logged flight",'Location','northoutside')
axis equal

x0=0;
y0=0;
plotwidth=500;
height=400;
set(gcf,'position',[x0,y0,plotwidth,height])
exportgraphics(gcf,'FlightGraphplot4.pdf','ContentType','image')

%% Track from above
figure(12)

plot(Flight.x_pos,Flight.y_pos, Track(:,1),Track(:,2))
grid on 
axis equal
xlabel('x position [m]')
ylabel('y position [m]')
%ylim([-1.6 -0.5])

x0=0;
y0=0;
plotwidth=500;
height=400;
set(gcf,'position',[x0,y0,plotwidth,height])
exportgraphics(gcf,'JacobSpecial.pdf','ContentType','image')

%% Clalculate xy speed on logged data

for n =1:length(Flight.x_pos)-1
    distSpeed(n) = sqrt( (Flight.x_pos(n)-Flight.x_pos(n+1))^2 + (Flight.y_pos(n)-Flight.y_pos(n+1))^2); %XY distance
    time(n)= Flight.time(n+1) - Flight.time(n);
    speed(n) = distSpeed(n)/(time(n));
end
time(length(Flight.x_pos))=0;
distSpeed(length(Flight.x_pos))=0;
speed(length(Flight.x_pos))=0;

speed = movmean(speed,10); %Average of approx 100 ms. Else the data is fucked.

figure(4)
plot(Flight.time, speed)%,Flight.time, distSpeed*100)
xlabel('time [s]')
ylabel('speed [m/s]')
ylim([0 1])
grid on 



%% Yaw  Yaw

%% Plottting yaw on track
yawTrack=Track(:,4);
figure(5)
t=1:length(yawTrack);
plot(t,Track(:,4),'.')
xlabel('point on Track')
ylabel('Yaw at point [deg]')
grid on

%% plotting yaw at nearest point on track
[NearestPointTrack, dist] = dsearchn(Track(:,1:3),[Flight.x_pos Flight.y_pos Flight.z_pos]);
yawAtPointTrack = yawTrack(NearestPointTrack);
figure(6)
plot(Flight.time,yawAtPointTrack,'.')
xlabel('time [s]')
ylabel('Yaw at closes point on Track [deg]')
grid on

% Plotting yaw at nearest point on track and measured yaw
figure(7)
plot(Flight.time,Flight.z_rot,'.', Flight.time,yawAtPointTrack,'.')
grid on
xlabel('time [s]')
ylabel('measured yaw')
legend('Measured yaw','Yaw at nearest point on track')

%% Plotting yaw error

yawError = abs(yawTrack(NearestPointTrack)-Flight.z_rot);   %Calculating error, error is abselout
for n=1:length(yawError)
    if yawError(n) > 179
        yawError(n) = abs(yawError(n)-360);  %360 deg error = 0 deg error                                  
    end
end 

figure(8)
plot(Flight.time, yawError,'.')
grid on
xlabel('time [s]')
ylabel('Abselout yaw error [deg]')

% point removed where speed is low
for n=1:length(Flight.time)
   if speed(n) < 0.1
        yawError(n) = -90;
   end
end

figure(9)
plot(Flight.time, yawError,'.')
xlabel('time [s]')
ylabel('Abselout yaw error [deg]');
ylim([0 200])
grid on

x0=0;
y0=0;
plotwidth=500;
height=400;
set(gcf,'position',[x0,y0,plotwidth,height])
exportgraphics(gcf,'YawErrorplot4.pdf','ContentType','vector')

%% Test of hover
HoverPoint=[1.025	1.725	1.000];

v=[Flight.x_pos Flight.y_pos Flight.z_pos]-HoverPoint;

distHover=vecnorm(v',1);

figure(10)
hold on
plot(Flight.time, distHover, '.')
grid on
ylim([0 0.3])
xlabel('Time  [s]')
ylabel('Distance to hover point [m]')

x0=0;
y0=0;
plotwidth=500;
height=400;
set(gcf,'position',[x0,y0,plotwidth,height])
exportgraphics(gcf,'Hoverplot4.pdf','ContentType','vector')

%% Yaw Method 2
for n=1:length(Flight.time)-50
    yawError2(n) = atan2(Flight.y_pos(n) - Flight.y_pos(n+50),Flight.x_pos(n) -Flight.x_pos(n+50))*180/pi; 
end 
yawError2(length(Flight.time)) =0;

figure(13)
plot(Flight.time, yawError2, '.', Flight.time, Flight.z_rot -90,'.')
grid on
disp('Hallo')

%% Close all
close all
