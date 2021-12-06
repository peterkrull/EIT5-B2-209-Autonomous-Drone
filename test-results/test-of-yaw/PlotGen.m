Track=readmatrix('PathUHD');
Track= Track(:,1:4);     %Reduce matrix a to needed values RAM OPT
Track(:,1:3) = Track(:,1:3)/1000;   %Calculate in meters

for n=1:length(Track(:,4))
    if Track(n,4) > 180
        Track(n,4) = Track(n,4)-360;
    end 
    Track(n,4) = Track(n,4)*(-1);
end

Flight=readtable('1638353769_accept_test_dec_1_test1');
Flight.x_pos = Flight.x_pos/1000; %Calculate in meter
Flight.y_pos = Flight.y_pos/1000;
Flight.z_pos = Flight.z_pos/1000;
Flight.z_rot = Flight.z_rot*180/pi;

disp("Hallow World")




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
exportgraphics(gcf,'Plot.pdf','ContentType','image')