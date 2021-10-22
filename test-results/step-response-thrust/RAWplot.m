array = csvread('hover to 150.csv');
time = array(:,1);
col = array(:,2);

figure(1)
hold on
plot(time,col,'x','color','#0072BD')
%plot(time,col)
%xlim([4 7])
ylabel("Thrust [g]")
xlabel("Time [s]")
title("Step from 41323 to 61984")
grid on
hold off


x0=0;
   y0=0;
   plotwidth=600;
   height=300;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'stepPitchUnProcessed.pdf','ContentType','vector')
