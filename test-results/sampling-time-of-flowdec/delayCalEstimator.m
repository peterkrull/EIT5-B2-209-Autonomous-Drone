clear
%Import data
A = readtable('1638195978_y_step_flowdeck.csv');

%Gemmer tider for data flow y
count1 = 1;
for i = 1:length(A.time)
   if not( isnan(A.motion_deltaY(i)) )
      FlowTimeY(count1) = A.time(i);
      count1 = count1 + 1;
   end
end

%Udregner delay y
for i = 2:length(FlowTimeY)
    delayY(i-1) = FlowTimeY(i)-FlowTimeY(i-1);
    tilPlotY(i-1) = (i-1);
end


%Gemmer tider for data flow x
count2 = 1;
for i = 1:length(A.time)
   if not( isnan(A.motion_deltaX(i)) )
      FlowTimeX(count2) = A.time(i);
      count2 = count2 + 1;
   end
end

%Udregner delay x
for i = 2:length(FlowTimeX)
    delayX(i-1) = FlowTimeX(i)-FlowTimeX(i-1);
    tilPlotX(i-1) = (i-1);
end

figure(1)
plot(tilPlotY,delayY,'x')
xlabel('Sampel [.]') 
ylabel('Delay [s]')
title('Delay flow y-axis')

x0=0;
   y0=0;
   plotwidth=400;
   height=300;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'delayY.pdf','ContentType','vector')

figure(2)
plot(tilPlotX,delayX,'x')
xlabel('Sampel [.]') 
ylabel('Delay [s]')
title('Delay flow x-axis')

x0=0;
   y0=0;
   plotwidth=400;
   height=300;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'delayX.pdf','ContentType','vector')