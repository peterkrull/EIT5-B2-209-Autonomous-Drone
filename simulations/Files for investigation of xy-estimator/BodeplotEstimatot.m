clear
%Laver bodeplot
s = tf('s');

%Definere 1 ordens LP-filter med cut off frekvens 2 Hz
tau = 1/(2*(2*pi));
LP = 1/(1+tau*s);

%Integrator
inte = 1/s;

%Omregning fra flow til hastighed
flow = 1;

%Delay vicon
tdv = 0.1;
vicon = (1-(tdv/2)*s)/(1+(tdv/2)*s);
%------------------------------------------------------

%Controller
Kp = 35;
Ki = 0;
Kd = 0.62;

D = Kp * ( 1 + Ki*(1/s) + Kd*s );

%Plant
H=0.02/(0.2*s+1);

%Matematiske model
M=9.82;

%Delay sampeling and radio
tdr = 0.002+((1/100)/2);
radio = (1-(tdr/2)*s)/(1+(tdr/2)*s);

opts = bodeoptions('cstprefs');
opts.PhaseWrapping='on';
opts.PhaseWrappingBranch = - 500;

figure(1)
bode(radio*D*H*M*inte*vicon*inte,opts)
grid on
xlim([1 10])
x0=0;
   y0=0;
   plotwidth=600;
   height=400;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'bodeEstimator.pdf','ContentType','vector')

figure(2)
margin(radio*D*H*M*inte*vicon*inte)

ol = radio*D*H*M*inte*vicon*inte;

cl = (radio*D*H*M*inte*vicon)/(1+ol);

figure(3)
P = 1/M*s^2*1/(1+2*pi*s)+1/(1+2*pi*3*s)*.22;
sensor = P*1/s*1/(1+1.5*2*pi*s);

ol = D*H*M/s;
cl = ol/(1+ol*sensor)*1/s;
step(cl)
grid on
xlim([0,2])


figure(4)
bode(cl)
grid on

figure(5)
sensor_lp = 1/(1+2*pi*1.5*s);
toPlot = .1*D*H*M*1/s^2*sensor_lp*H;
bode(toPlot)
grid on

figure(6)
step(D*H*M*1/s^2/(1+P*1/(1+1.5*2*pi*s)*D*H*M*1/s^2))