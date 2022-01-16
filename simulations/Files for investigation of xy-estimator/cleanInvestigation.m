%clear
%Laver bodeplot
s = tf('s');


%Controller
Kp = 35;
Ki = 0;
Kd = 0.62;

D = Kp * ( 1 + Ki*(1/s) + Kd*s );

controllerPhaseDelay = exp(-s*0.002);

%Plant
H=0.02/(0.2*s+1);

%Matematiske model
M=9.82;


%sensor
H_lp1 = 1*2*pi/(1*2*pi+s);
H_lp3 = 3*2*pi/(3*2*pi+s);

G = 1/M * s^2*H_lp1*1.5+H_lp3;

sensorPhaseDelay = exp(-s*0.015);


OL = D*H*M*(1/s^2)*G*H_lp3*sensorPhaseDelay*controllerPhaseDelay;
CL = D*H*M*(1/s^2)*controllerPhaseDelay/(1+OL);





figure(1)
margin(OL)
xlim([.1 100])
grid on

figure(2)
step(CL)
grid on



figure(3)
G2 = 1+ 1/M * s^2;
H_lpsens = 0.5*2*pi/(0.5*2*pi+s);

OL2 = D*H*M*(1/s^2)*H_lpsens;%*sensorPhaseDelay*controllerPhaseDelay
%OL2 = D*H*M*(1/s^2)*G2*sensorPhaseDelay*controllerPhaseDelay
CL2 = D*H*M*(1/s^2)*controllerPhaseDelay/(1+OL2);
margin(OL2)
grid on
xlim([1 100])
export_fig('xy-estimatorOpenloop.pdf')


figure(4)
step(CL2)
grid on

export_fig('xy-estimatorStep.pdf')



function export_fig(name)
    x0=0;
    y0=0;
    plotwidth=650;
    plotHeight=400;
    set(gcf,'position',[x0,y0,plotwidth,plotHeight])
    
    
    exportgraphics(gcf,name,'ContentType','vector')
end