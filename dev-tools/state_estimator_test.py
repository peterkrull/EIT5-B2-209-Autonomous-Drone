from state_estimator import state_estimator
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\test-of-barometer\\1637152127_baro_meas.csv'
#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\onboard-sensor-drift\\1637063677_test_flyvning.csv'
with open(file, newline='') as csvFile:
    dataReader = csv.DictReader(csvFile, delimiter=",")
    testDataHeader = dataReader.fieldnames
    testData = list(csv.reader(csvFile,delimiter=","))
    testData = [x for x in testData if '' not in x]
    testData = np.array(testData).astype(np.float)

#[række,søjle]

pos = {'x':testData[0][1], 'y': testData[0][2], 'z': testData[0][3], 'yaw': testData[0][6]}

state_est = state_estimator(pos, k = .33)

gx_index = testDataHeader.index("gyro_x")
gy_index = testDataHeader.index("gyro_y")
gz_index = testDataHeader.index("gyro_z")
ax_index = testDataHeader.index("acc_x")
ay_index = testDataHeader.index("acc_y")
az_index = testDataHeader.index("acc_z")
seYaw_index = testDataHeader.index("stateEstimate_yaw")


est_pos = []


for i in testData:
    vicon_pos = []
    for j in range(7):
        vicon_pos.append(i[j])
    #print(vicon_pos)
    drone_data = {'gyro_x':i[gx_index], 'gyro_y':i[gy_index], 'gyro_z':i[gz_index],'acc_x':i[ax_index], 'acc_y':i[ay_index], 'acc_z':i[az_index], 'stateEstimate_yaw':i[seYaw_index],'time':i[0]} 

    a = state_est.update(vicon_pos,drone_data,1)
    #print(a)
    est_pos.append(a.copy())

x_diff = []
y_diff = []
z_diff = []
yaw_diff = []

for i in range(len(testData)):
    x_diff.append(testData[i][1]-est_pos[i]['x'])
    y_diff.append(testData[i][2]-est_pos[i]['y'])
    z_diff.append(testData[i][3]-est_pos[i]['z'])
    yaw_diff.append(testData[i][6]-est_pos[i]['yaw'])

#print(x_diff)
#print(y_diff)
#print(z_diff)ccc

x_axis = np.linspace(testData[0][0],testData[len(testData)-1][0],len(testData))
#print(x_diff)

plotX = [a['x']for a in est_pos]
plt.figure(1)
ax = plt.subplot(411)
x1, = plt.plot(x_axis, [a['x']for a in est_pos], label ="estimated x")
x2, =plt.plot(x_axis, testData[:,1], label = "Measured x")
plt.grid()
plt.legend(handles = [x1,x2])
ax = plt.gca()
ax.set_ylim([-3000,3000])
plt.subplot(412)
y1, = plt.plot(x_axis, [a['y']for a in est_pos], label = "estimated y")
y2, = plt.plot(x_axis, testData[:,2], label = "Measured y")
plt.grid()
plt.legend(handles = [y1,y2])
ax = plt.gca()
ax.set_ylim([-3000,3000])
plt.subplot(413)
z1, = plt.plot(x_axis, [a['z']for a in est_pos], label = "estimated z")
z2, = plt.plot(x_axis, testData[:,3], label = "Measured z")
plt.grid()
plt.legend(handles = [z1,z2])
plt.subplot(414)
yaw1, = plt.plot(x_axis, [a['yaw']for a in est_pos], label = "estimated yaw")
yaw2, = plt.plot(x_axis, 180/np.pi *testData[:,6], label = "Measured yaw")
plt.grid()
plt.legend(handles = [yaw1,yaw2])

plt.show()