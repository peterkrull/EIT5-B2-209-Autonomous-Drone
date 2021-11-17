T = readtable('1637063677_test_flyvning.csv');

%Fill missing data
T.gyro_x = fillmissing(T.gyro_x,'linear');
T.gyro_y = fillmissing(T.gyro_y,'linear');
T.gyro_z = fillmissing(T.gyro_z,'linear');
T.acc_x = fillmissing(T.acc_x,'linear');
T.acc_y = fillmissing(T.acc_y,'linear');
T.acc_z = fillmissing(T.acc_z,'linear');
T.stateEstimate_yaw = fillmissing(T.stateEstimate_yaw,'linear');
T.baro_pressure = fillmissing(T.baro_pressure,'linear');
T.pm_vbat = fillmissing(T.pm_vbat,'linear');

hold on
%figure(1)
plot(T.time,T.z_pos)
%figure(2)
plot(T.time,(-T.baro_pressure+1022.48)*5642)
ylim([600 1800])
hold off