data = readmatrix('1636707423_sensorDrift.csv');

startTime = data(1,1);
t = data(:,1)-startTime;

figure(1)
plot(t,data(:,2))
hold on
plot(t,data(:,2))
plot(t,data(:,3))
title('Gyroscope drift');
legend('gyro.x','gyro,y','gyro.z')
hold off

gyroXRateOfChange = 

figure(4)
plot(t,data(:,4))
hold on
plot(t,data(:,5))
plot(t,data(:,6))
title('Accelerometer drift')
hold off
legend('acc.x','acc.y','acc.z')

