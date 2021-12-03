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
tdv = 0.02;
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
bode(radio*D*H*M*inte*vicon*flow*LP*inte,opts)
grid on
xlim([1 10])
x0=0;
   y0=0;
   plotwidth=600;
   height=400;
   set(gcf,'position',[x0,y0,plotwidth,height])
   
exportgraphics(gcf,'bodeEstimator.pdf','ContentType','vector')

figure(2)
margin(radio*D*H*M*inte*vicon*flow*LP*inte)

ol = radio*D*H*M*inte*vicon*flow*LP*inte;

cl = (radio*D*H*M*inte*vicon)/(1+ol);

figure(3)
step(cl*(1/s))