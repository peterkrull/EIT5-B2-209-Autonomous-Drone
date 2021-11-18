data = readmatrix('1637063677_test_flyvning.csv');

timeBetweenMeasurements = zeros(length(data),1);
for i = 1: length(timeBetweenMeasurements)-1
   timeBetweenMeasurements(i) = data(i+1,1)-data(i,1); 
end

sample = linspace(0,length(data),length(data))';

plot(sample, timeBetweenMeasurements);
grid on