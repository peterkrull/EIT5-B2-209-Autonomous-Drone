%Made using following source, equation 40
%https://fenix.tecnico.ulisboa.pt/downloadFile/1970719973965869/Resumo%20Alargado.pdf


height11 = '1637840817_højde1_1';
height12 = '1637840857_højde1_2';

height21 = '1637840913_højde2_1';
height22 = '1637841006_højde2_2';
height23 = '1637841045_højde2_3';

k_of = [];
figure(1)
k_of = [k_of;plotFlowData(strcat(height11,'.csv'))];
figure(2)
k_of = [k_of;plotFlowData(strcat(height12,'.csv'))];
figure(3)
k_of = [k_of;plotFlowData(strcat(height21,'.csv'))];
figure(4)
k_of = [k_of;plotFlowData(strcat(height22,'.csv'))];
figure(5)
k_of = [k_of;plotFlowData(strcat(height23,'.csv'))];

k_of

ave_k_of_x = sum(abs(k_of(:,1)))/length(k_of); 
ave_k_of_y = sum(abs(k_of(:,2)))/length(k_of);

fprintf('average koefficient in x: %f\n', ave_k_of_x)
fprintf('average koefficient in y: %f\n\n', ave_k_of_y)



function plotDataFig(data_in,velAverage,fixed_flow)
    subplot(5,1,1)
    plot(data_in(:,1), data_in(:,2))
    hold on
    plot(data_in(:,1), data_in(:,3))
    hold off
    grid on
    title('flowdeck')
    
    subplot(5,1,2)
    plot(data_in(:,1), data_in(:,4))
    hold on
    plot(data_in(:,1), data_in(:,5))
    hold off
    grid on
    title('differentiated vicon')
    
    subplot(5,1,3)
    plot(data_in(:,1), velAverage(:,1))
    hold on
    plot(data_in(:,1), velAverage(:,2))
    hold off
    grid on
    title('average flowdeck')
    
    subplot(5,1,4)
    plot(data_in(:,1), velAverage(:,3))
    hold on
    plot(data_in(:,1), velAverage(:,4))
    hold off
    grid on
    title('average vicon')
    
    subplot(5,1,5)
    plot(data_in(:,1), fixed_flow)
    grid on
    title('koefficient')
end

function k_of = plotFlowData(fileName)
    data = readmatrix(fileName);

    height = sum(data(:,4))/(1000*length(data));
    
    plotData = [];
    %Sorterer punkter fra hvor der ikke er sensor data
    for i = 1: length(data)
        if ~isnan(data(i,size(data,2)))
            plotData = [plotData; data(i,1) data(i,2), data(i,3), data(i,40),data(i,41)];
        end
    end

    viconVel = [0 0];

    for i = 2:length(plotData)
        xvel = (plotData(i,2) - plotData(i-1,2))/(plotData(i,1)-plotData(i-1,1));
        yvel = (plotData(i,3) - plotData(i-1,3))/(plotData(i,1)-plotData(i-1,1));
        viconVel = [viconVel; xvel yvel];
    end

    viconVel = viconVel/1000;
    
    out = [plotData(:,1), plotData(:,4), plotData(:,5), viconVel(:,1), viconVel(:,2)];
    
    ave_flow_x = sum(out(:,2))/length(out);
    ave_flow_y = sum(out(:,3))/length(out);
    ave_speed_x = sum(out(:,4))/length(out);
    ave_speed_y = sum(out(:,5))/length(out);
    
    if abs(ave_flow_x) > abs(ave_flow_y) && abs(ave_speed_x)<abs(ave_speed_y)
       buffer = out(:,2);
       out(:,2) = out(:,3);
       out(:,3) = buffer;
    elseif abs(ave_flow_x) < abs(ave_flow_y) && abs(ave_speed_x)>abs(ave_speed_y)
        
    end

    
    num2average = 50;
    averageVel = zeros(num2average,4);
    
    for i = 1:length(out)-num2average
        ave_vicon_x = 0;
        ave_vicon_y = 0;
        ave_flow_x = 0;
        ave_flow_y = 0;
        for j = 1:num2average
            ave_flow_x = ave_flow_x + out(i,2);
            ave_flow_y = ave_flow_y + out(i,3);
            ave_vicon_x = ave_vicon_x + out(i,4);
            ave_vicon_y = ave_vicon_y + out(i,5);
        end 
        averageVel = [averageVel;ave_flow_x/num2average ave_flow_y/num2average ave_vicon_x/num2average ave_vicon_y/num2average];
    end
    
    k_of_vec = [];
    
    for i = num2average:length(averageVel)
        k_of_vec = [k_of_vec;-1*averageVel(i,3)/(averageVel(i,1)*height) -1*averageVel(i,4)/(averageVel(i,2)*height)];
    end
    
    
    ave_flow_x = sum(out(:,2))/length(out);
    ave_flow_y = sum(out(:,3))/length(out);
    ave_speed_x = sum(out(:,4))/length(out);
    ave_speed_y = sum(out(:,5))/length(out);
    
    
    k_of = [ave_speed_x/ave_flow_x*(1/(-1*height)) ave_speed_y/ave_flow_y*1/(-1*height)];
    
    fixed_flow = [];
    fixed_flow(:,1) = -height*k_of(1)*out(:,2);
    fixed_flow(:,2) = -height*k_of(2)*out(:,3);
    
    plotDataFig(out,averageVel,fixed_flow)
    
    fprintf('%s\n',fileName)
    fprintf('average height: %f\n', height)
    fprintf('average flow in x: %f\n',ave_flow_x)
    fprintf('average flow in y: %f\n',ave_flow_y)
    fprintf('average speed in x: %f\n',ave_speed_x)
    fprintf('average speed in y: %f\n',ave_speed_y)
    fprintf('average k_of in x: %f\n', k_of(1))
    fprintf('average k_of in y: %f\n\n', k_of(2))
end
