s = tf('s');

G = (0.00000816)/(0.136*s+1);
figure(1)
step(G)
title("Step response of plant")
grid on

G = G*(1/s^2);
%Ustabil da der er to poler i 0 hvilket giver et fasedrej på -180 grader med
%uendelig DC-gain
figure(2)
margin(G)
%title("Step response of plant with double integration")
grid on




%Lead-controller indføres for at fjerne én pol i nul
D = s/(s+1)*exp(-s*1.002);
figure(3)
margin(G*D)
grid on
title("Plant with lead-controller (k = 1)")

k_lead = 100000;
a_lead = 0;
b_lead = 1;

D_lead = k_lead *(s+a_lead)/(s+b_lead);
O = D_lead*G;
figure(4)
margin(O)
grid on


figure(6)
step(O/(1+O*exp(-s*0.0083)))
grid on
title("Step response of close loop")
