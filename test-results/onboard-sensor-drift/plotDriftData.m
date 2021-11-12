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

gyroIntegral = [data(1,2) data(1,3) data(1,4)];
for i = 2:length(data)
   gyroIntegral = [gyroIntegral; gyroIntegral(i-1,1)+data(i,2) gyroIntegral(i-1,2)+data(i,3) gyroIntegral(i-1,3)+data(i,4)];  
end

figure(5)
subplot(3,1,1)
plot(t,gyroIntegral(:,1))
title('gyro.x pos')

subplot(3,1,2)
plot(t,gyroIntegral(:,2))
title('gyro.y pos')


subplot(3,1,3)
plot(t,gyroIntegral(:,3))
title('gyro.z pos')



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

