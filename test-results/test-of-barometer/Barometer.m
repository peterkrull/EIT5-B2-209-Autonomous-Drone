clear
%Import data
A = readtable('0cmAboveGroundNoThrust.csv');
B = readtable('1637152127_baro_meas.csv');


%Fill missing data
B.gyro_x = fillmissing(B.gyro_x,'linear');
B.gyro_y = fillmissing(B.gyro_y,'linear');
B.gyro_z = fillmissing(B.gyro_z,'linear');
B.acc_x = fillmissing(B.acc_x,'linear');
B.acc_y = fillmissing(B.acc_y,'linear');
B.acc_z = fillmissing(B.acc_z,'linear');
B.stateEstimate_yaw = fillmissing(B.stateEstimate_yaw,'linear');
B.baro_pressure = fillmissing(B.baro_pressure,'linear');
B.pm_vbat = fillmissing(B.pm_vbat,'linear');

%Udregner gennemsnittet af data for 0cm over gulvet uden thrust
sum = 0;
for i = 1:length(A.Var9)
    sum = sum + A.Var9(i);
end
gennemsnit = sum/length(A.Var9);

%Plot data for 0cm over gulvet uden thrust
hold on
plot(A.Var1-1.637152303085561e+09,A.Var9)
fplot(@(x) gennemsnit)
xlim([0,30])
xlabel('Time [s]') 
ylabel('Pressure [mbar]') 
hold off

%Plot z-højde Vicon som funktion af tid
figure(2)
plot(B.time,B.z_pos)


figure(3)
plot(B.time,-B.baro_pressure)

% 49mm 2.60156 - 6.35138
% 143mm 10.582 - 16.5513
% 366mm 21.05 - 25.8705
% 565mm 31.1304 - 37.4199
% 763mm 40.5612 - 46.001
% 967mm 50.9813 - 56.2317
% 1173mm 61.4008 - 66.7112
% 1371mm 71.0908 - 77.2713
% 1568mm 81.2303 - 85.1812
% 1776mm 89.771 - 96.9609
% 1990mm 99.8007 - 105.381
% 2184mm 109.09 - 115.351
% 2392mm 118.5 - 124.07

%Barometer data for 49mm
BarSum1 = 0;
for i = 247:622
    BarSum1 = BarSum1 + B.baro_pressure(i);
end
BarGennemsnit1 = BarSum1/(622-247)

%Barometer data for 143mm
BarSum2 = 0;
for i = 1045:1642
    BarSum2 = BarSum2 + B.baro_pressure(i);
end
BarGennemsnit2 = BarSum2/(1642-1045)

%Barometer data for 366mm
BarSum3 = 0;
for i = 2092:2574
    BarSum3 = BarSum3 + B.baro_pressure(i);
end
BarGennemsnit3 = BarSum3/(2574-2092)

%Barometer data for 565mm
BarSum4 = 0;
for i = 3100:3729
    BarSum4 = BarSum4 + B.baro_pressure(i);
end
BarGennemsnit4 = BarSum4/(3729-3100)

%Barometer data for 763mm
BarSum5 = 0;
for i = 4034:4587
    BarSum5 = BarSum5 + B.baro_pressure(i);
end
BarGennemsnit5 = BarSum5/(4587-4034)

%Barometer data for 967mm
BarSum6 = 0;
for i = 5085:5614
    BarSum6 = BarSum6 + B.baro_pressure(i);
end
BarGennemsnit6 = BarSum6/(5614-5085)

%Barometer data for 1173mm
BarSum7 = 0;
for i = 6027:6658
    BarSum7 = BarSum7 + B.baro_pressure(i);
end
BarGennemsnit7 = BarSum7/(6658-6027)

%Barometer data for 1371mm
BarSum8 = 0;
for i = 7096:7714
    BarSum8 = BarSum8 + B.baro_pressure(i);
end
BarGennemsnit8 = BarSum8/(7714-7096)

%Barometer data for 1568mm
BarSum9 = 0;
for i = 8110:8505
    BarSum9 = BarSum9 + B.baro_pressure(i);
end
BarGennemsnit9 = BarSum9/(8505-8110)

%Barometer data for 1776mm
BarSum10 = 0;
for i = 8964:9683
    BarSum10 = BarSum10 + B.baro_pressure(i);
end
BarGennemsnit10 = BarSum10/(9683-8964)

%Barometer data for 1990mm
BarSum11 = 0;
for i = 9967:10525
    BarSum11 = BarSum11 + B.baro_pressure(i);
end
BarGennemsnit11 = BarSum11/(10525-9967)

%Barometer data for 2184mm
BarSum12 = 0;
for i = 10897:11522
    BarSum12 = BarSum12 + B.baro_pressure(i);
end
BarGennemsnit12 = BarSum12/(11522-10897)

%Barometer data for 2392mm
BarSum13 = 0;
for i = 11837:12394
    BarSum13 = BarSum13 + B.baro_pressure(i);
end
BarGennemsnit13 = BarSum13/(12394-11837)

%Definer array af tryk
ArrayTryk = [BarGennemsnit1, BarGennemsnit2, BarGennemsnit3, BarGennemsnit4, BarGennemsnit5, BarGennemsnit6, BarGennemsnit7, BarGennemsnit8, BarGennemsnit9, BarGennemsnit10, BarGennemsnit11, BarGennemsnit12, BarGennemsnit13];

%Definer array af højde
ArrayHeight = [49, 143, 366, 565, 763, 967, 1173, 1371, 1568, 1776, 1990, 2184, 2392];

%Plot Tryk som funktion af højde
figure(4)
plot(ArrayHeight,-ArrayTryk)

figure(5)
plot(B.z_pos,-B.baro_pressure,'x')
