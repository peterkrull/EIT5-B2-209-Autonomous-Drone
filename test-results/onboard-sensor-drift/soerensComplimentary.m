data = readmatrix('1636980205_sensorDrift');

data(:,1) = data(:,1)-data(1,1);
prevAngle = 0;
timeDif = data(2,1)-data(1,1);
a = .1;

for i = 1 :length(data)
    estAngle(i) = a*atan(data(i,6)/(data(i,7))) +(1-a)*(prevAngle + data(i,3)*timeDif); 
    prevAngle = estAngle(i);
end

estAngle = estAngle*180/pi;
plot(data(:,1),estAngle)