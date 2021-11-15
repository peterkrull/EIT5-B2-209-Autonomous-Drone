format long
data = readmatrix('1636709437_sensorDrift.csv');
data2 = readmatrix('1636710817_sensorDrift');


figure(1)
res1 = plotData(data);
figure(2)
res2 = plotData(data2);

function [gyroDriftX, gyroDriftY, gyroDriftZ, accXOffset, accYOffset, accZOffset] = plotData(data)
    startTime = data(1,1);
    t = data(:,1)-startTime;

    subplot(4,6,1)
    plot(t,data(:,2))
    hold on
    plot(t,data(:,3))
    plot(t,data(:,4))
    title('Gyroscope drift');
    legend('gyro.x','gyro,y','gyro.z')
    hold off

    subplot(4,6,4)
    plot(t,data(:,2))
    title('gyro.x');
    gyroXlr = polyfit(t, data(:,2),1);
    linreg = polyval(gyroXlr, t);
    disp('Linear regression gyro.x')
    disp(gyroXlr)
    hold on
    plot(t,linreg)
    hold off
    
    subplot(4,6,5)
    plot(t,data(:,3))
    title('gyro.y');
    gyroYlr = polyfit(t, data(:,3),1);
    linreg = polyval(gyroYlr, t);
    disp('Linear regression gyro.y')
    disp(gyroYlr)
    hold on
    plot(t,linreg)
    hold off
    
    
    subplot(4,6,6)
    plot(t,data(:,4))
    title('gyro.z');
    gyroZlr = polyfit(t, data(:,4),1);
    linreg = polyval(gyroZlr, t);
    disp('Linear regression gyro.z')
    disp(gyroZlr)
    hold on
    plot(t,linreg)
    hold off
    
    
    
    gyroIntegral = [data(1,2) data(1,3) data(1,4)];
    for i = 2:length(data)
       gyroIntegral = [gyroIntegral; gyroIntegral(i-1,1)+data(i,2) gyroIntegral(i-1,2)+data(i,3) gyroIntegral(i-1,3)+data(i,4)];  
    end
    gyroIntegral = gyroIntegral*(t(2)-t(1));

    subplot(4,6,7)
    plot(t,gyroIntegral(:,1))
    title('gyro.x pos')
    
    subplot(4,6,8)
    plot(t,gyroIntegral(:,2))
    title('gyro.y pos')


    subplot(4,6,9)
    plot(t,gyroIntegral(:,3))
    title('gyro.z pos')

    gyroXOffset = sum(data(:,2))/length(data);
    gyroDriftX = gyroXOffset;
    gyroYOffset = sum(data(:,3))/length(data);
    gyroDriftY = gyroYOffset;
    gyroZOffset = sum(data(:,4))/length(data);
    gyroDriftZ = gyroZOffset;

    gyroIntegral2 = [data(1,2)-gyroXOffset data(1,3)-gyroYOffset data(1,4)-gyroZOffset];
    for i = 2:length(data)
       gyroIntegral2 = [gyroIntegral2; gyroIntegral2(i-1,1)+data(i,2)-gyroXOffset gyroIntegral2(i-1,2)+data(i,3)-gyroYOffset gyroIntegral2(i-1,3)+data(i,4)-gyroZOffset];  
    end
    gyroIntegral2 = gyroIntegral2*(t(2)-t(1));

    subplot(4,6,10)
    plot(t,gyroIntegral2(:,1))
    title('gyro.x pos no offset')

    subplot(4,6,11)
    plot(t,gyroIntegral2(:,2))
    title('gyro.y pos no offset')


    subplot(4,6,12)
    plot(t,gyroIntegral2(:,3))
    title('gyro.z pos no offset')

    for i = 1 : length(t)-10
        gOffx = 0;
        gOffy = 0;
        gOffz = 0;
        for j = 1:10
            gOffx = gOffx + data(i+j,2);
            gOffy = gOffy + data(i+j,3);
            gOffz = gOffz + data(i+j,4);
        end
        gOffSet(i,1) = gOffx/10;
        gOffSet(i,2) = gOffy/10;
        gOffSet(i,3) = gOffz/10;
    end 
    timeTemp = t(1:length(t)-10);
    
    subplot(4,6,13)
    plot(timeTemp,gOffSet(:,1))
    title('gyro.x pos running offset')

    subplot(4,6,14)
    plot(timeTemp,gOffSet(:,2))
    title('gyro.y pos running offset')


    subplot(4,6,15)
    plot(timeTemp,gOffSet(:,3))
    title('gyro.z pos running offset')
    
    

    subplot(4,6,2)
    plot(t,data(:,5))
    hold on
    plot(t,data(:,6))
    plot(t,data(:,7))
    title('Accelerometer drift')
    hold off
    legend('acc.x','acc.y','acc.z')

    subplot(4,6,16)
    plot(t,data(:,5))
    title('acc.x');
    accXlr = polyfit(t, data(:,5),1);
    linreg = polyval(accXlr, t);
    disp('Linear regression acc.x')
    disp(accXlr)
    hold on
    plot(t,linreg)
    hold off
    
    
    subplot(4,6,17)
    plot(t,data(:,6))
    title('acc.y');
    accYlr = polyfit(t, data(:,6),1);
    linreg = polyval(accYlr, t);
    disp('Linear regression acc.y')
    disp(accYlr)
    hold on
    plot(t,linreg)
    hold off
    
    
    
    subplot(4,6,18)
    plot(t,data(:,7))
    title('acc.z');
    accZlr = polyfit(t, data(:,7),1);
    linreg = polyval(accZlr, t);
    disp('Linear regression acc.z')
    disp(accZlr)
    hold on
    plot(t,linreg)
    hold off
    

    accIntegral = [data(1,5) data(1,6) data(1,7)];
    for i = 2:length(data)
       accIntegral = [accIntegral; accIntegral(i-1,1)+data(i,5) accIntegral(i-1,2)+data(i,6) accIntegral(i-1,3)+data(i,7)];  
    end
    accIntegral = accIntegral*(t(2)-t(1));

    velIntegral = [accIntegral(1,1) accIntegral(1,2) accIntegral(1,3)];
    for i = 2:length(accIntegral)
       velIntegral = [velIntegral; velIntegral(i-1,1)+accIntegral(i,1) velIntegral(i-1,2)+accIntegral(i,2) velIntegral(i-1,3)+accIntegral(i,3)];  
    end
    velIntegral = velIntegral*(t(2)-t(1))*9.82;


    subplot(4,6,19)
    plot(t,velIntegral(:,1))
    title('drone.x pos')

    subplot(4,6,20)
    plot(t,velIntegral(:,2))
    title('drone.y pos')


    subplot(4,6,21)
    plot(t,velIntegral(:,3))
    title('drone.z pos')

    accXOffset = sum(data(:,5))/length(data);
    accYOffset = sum(data(:,6))/length(data);
    accZOffset = sum(data(:,7))/length(data);
    

    accIntegral2 = [data(1,5)-accXOffset data(1,6)-accYOffset data(1,7)-accZOffset];
    for i = 2:length(data)
       accIntegral2 = [accIntegral2; accIntegral2(i-1,1)+data(i,5)-accXOffset accIntegral2(i-1,2)+data(i,6)-accYOffset accIntegral2(i-1,3)+data(i,7)-accZOffset];  
    end
    accIntegral2 = accIntegral2*(t(2)-t(1));

    subplot(4,6,22)
    plot(t,accIntegral2(:,1))
    title('acc.x pos no offset')
    
    subplot(4,6,23)
    plot(t,gyroIntegral2(:,2))
    title('acc.y pos no offset')


    subplot(4,6,24)
    plot(t,gyroIntegral2(:,3))
    title('acc.z pos no offset')
end 