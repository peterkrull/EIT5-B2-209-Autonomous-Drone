data = readmatrix('1636709437_sensorDrift.csv');

startTime = data(1,1);
t = data(:,1)-startTime;

figure(1)
plot(t,data(:,2))
hold on
plot(t,data(:,3))
plot(t,data(:,4))
title('Gyroscope drift');
legend('gyro.x','gyro,y','gyro.z')
hold off

figure(2)
subplot(3,1,1)
plot(t,data(:,2))
title('gyro.x');

subplot(3,1,2)
plot(t,data(:,3))
title('gyro.y');

subplot(3,1,3)
plot(t,data(:,4))
title('gyro.z');



plot(t,gyroXdiff)





figure(3)
plot(t,data(:,5))
hold on
plot(t,data(:,6))
plot(t,data(:,7))
title('Accelerometer drift')
hold off
legend('acc.x','acc.y','acc.z')

figure(4)
subplot(3,1,1)
plot(t,data(:,5))
title('acc.x');

subplot(3,1,2)
plot(t,data(:,6))
title('acc.y');

subplot(3,1,3)
plot(t,data(:,7))
title('acc.z');

