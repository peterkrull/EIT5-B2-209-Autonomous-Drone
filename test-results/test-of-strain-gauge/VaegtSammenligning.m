clear
%%Tom vægt
arrayTom = csvread('Tommåling.csv');
colTom = arrayTom(:,2);

sumTom = 0;
for i=1:length(colTom)
    sumTom = sumTom + colTom(i);
end

Tom = sumTom/length(colTom)
%Havenisse 0g

figure(1)
plot(arrayTom(:,1),arrayTom(:,2),'x')
ylabel("Weight [kg]")
xlabel("Time [s]")
title("Empty")
x0=0;
   y0=0;
   plotwidth=400;
   height=300;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'empty.pdf','ContentType','vector')
%---------------------------------------------------------------------
%%Razer vægt
arrayRazer = csvread('Razermåling.csv');
colRazer = arrayRazer(:,2);

sumRazer = 0;
for i=1:length(colRazer)
    sumRazer = sumRazer + (colRazer(i)-Tom);
end

Razer = sumRazer/length(colRazer)
%Havenisse 249g

figure(2)
plot(arrayRazer(:,1),arrayRazer(:,2),'x')
ylabel("Weight [kg]")
xlabel("Time [s]")
title("Mass 1")
x0=0;
   y0=0;
   plotwidth=400;
   height=300;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'mass1.pdf','ContentType','vector')
%---------------------------------------------------------------------
%%Oukitel vægt
arrayOukitel = csvread('Oukitelmåling.csv');
colOukitel = arrayOukitel(:,2);

sumOukitel = 0;
for i=1:length(colOukitel)
    sumOukitel = sumOukitel + (colOukitel(i)-Tom);
end

Oukitel = sumOukitel/length(colOukitel)
%Havenisse 287,9g

figure(3)
plot(arrayOukitel(:,1),arrayOukitel(:,2),'x')
ylabel("Weight [kg]")
xlabel("Time [s]")
title("Mass 2")
x0=0;
   y0=0;
   plotwidth=400;
   height=300;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'mass2.pdf','ContentType','vector')