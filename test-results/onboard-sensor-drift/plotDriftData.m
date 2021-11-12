data = readmatrix('1636707423_sensorDrift.csv');

startTime = data(1,1);
t = data(:,1)-startTime;

figure(1)
plot(t,data(:,2))
title('gyro.x')

figure(2)
plot(t,data(:,2))
title('gyro.y')

figure(3)
plot(t,data(:,3))
title('gyro.z')

figure(4)
plot(t,data(:,4))
title('acc.x')

figure(5)
plot(t,data(:,5))
title('acc.y')

figure(6)
plot(t,data(:,6))
title('acc.z')