data = readmatrix('1637063677_test_flyvning');


data(:,1) = data(:,1)-data(1,1);
prevAngle = [0 0];
timeDif = data(2,1)-data(1,1);
a = .33;

for i = 1 :length(data)
    if(~isnan(data(i,30)))
        estAngle(i,1) = a*atan(data(i,29)/(data(i,31))) +(1-a)*(prevAngle(1) + data(i,26)*timeDif); 
        prevAngle(1) = estAngle(i,1);
        
        estAngle(i,2) = a*atan(data(i,30)/(data(i,31))) +(1-a)*(prevAngle(2) + data(i,27)*timeDif); 
        prevAngle(2) = estAngle(i,2);
    end
end

estAngle = estAngle*180/pi;
x_axis = linspace(data(1,1), data(length(data),1),length(estAngle)); 
figure(1)
plot(x_axis,estAngle(:,1))
hold on 
plot(data(:,1), data(:,5)*180/pi)
hold off 
grid on 
title('Pitch angle')
legend('Estimated pitch','Measured pitch')

figure(2)
plot(x_axis,estAngle(:,2))
hold on 
plot(data(:,1), data(:,6)*180/pi)
hold off 
grid on 
title('Roll angle')
legend('Estimated roll','Measured roll')