from state_estimator import state_estimator
import csv
import numpy as np
import matplotlib.pyplot as plt
import time
import random

#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\test-of-barometer\\1637152127_baro_meas.csv'
#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\onboard-sensor-drift\\1637063677_test_flyvning.csv'
file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\onboard-sensor-drift\\1637674848_fly_track_with_estimator.csv'

with open(file, newline='') as csvFile:
    dataReader = csv.DictReader(csvFile, delimiter=",")
    testDataHeader = dataReader.fieldnames
    testData = list(csv.reader(csvFile,delimiter=","))
    testData = [x for x in testData if '' not in x]
    testData = np.array(testData).astype(np.float)

#[række,søjle]

pos = {'x':testData[0][1], 'y': testData[0][2], 'z': testData[0][3], 'yaw': testData[0][6]}
viconInit = [testData[0][0], testData[0][1], testData[0][2], testData[0][3], testData[0][4], testData[0][5],testData[0][6]]
state_est = state_estimator(pos, viconInit, Kx = .1, Ky =.1)

gx_index = testDataHeader.index("gyro_x")
gy_index = testDataHeader.index("gyro_y")
ax_index = testDataHeader.index("acc_x")
ay_index = testDataHeader.index("acc_y")
az_index = testDataHeader.index("acc_z")
seYaw_index = testDataHeader.index("stateEstimate_yaw")
baro_index = testDataHeader.index("baro_pressure")
se_vc_index = testDataHeader.index("stateEstimate_vz")

est_pos = []
time_axis = []
vicon_available = 1
for i in testData:
    vicon_pos = []
    for j in range(7):
        vicon_pos.append(i[j])
    
    if vicon_available == 1:
        lotto_viconAvailable = random.randrange(0,500,1)
        if lotto_viconAvailable == 69 and i[0]>5:
        #if i[0]>27:
            vicon_available = 0
            print("switch time:", i[0])

    #print(vicon_pos)
    drone_data = {'gyro.x':i[gx_index], 'gyro.y':i[gy_index], 'acc.x':i[ax_index], 'acc.y':i[ay_index], 'acc.z':i[az_index], 'stateEstimate.yaw':i[seYaw_index],'time':i[0], 'baro.pressure':i[baro_index], 'stateEstimate.vz':i[se_vc_index]} 

    a = state_est.update(vicon_pos,drone_data,vicon_available)
    
    if vicon_available == 1:
        pass
    else:
        #time.sleep(.5)
        pass

    est_pos.append(a.copy())
    time_axis.append(i[0])


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
ax = plt.subplot(311)
x1, = plt.plot(time_axis, [a['x']for a in est_pos], label ="estimated x")
x2, =plt.plot(time_axis, testData[:,1], label = "Measured x")
plt.grid()
plt.legend(handles = [x1,x2])
ax = plt.gca()
ax.set_ylim([-3000,3000])
plt.subplot(312)
y1, = plt.plot(time_axis, [a['y']for a in est_pos], label = "estimated y")
y2, = plt.plot(time_axis, testData[:,2], label = "Measured y")
plt.grid()
plt.legend(handles = [y1,y2])
ax = plt.gca()
ax.set_ylim([-3000,3000])
plt.subplot(313)
z1, = plt.plot(time_axis, [a['z']for a in est_pos], label = "estimated z")
z2, = plt.plot(time_axis, testData[:,3], label = "Measured z")
plt.grid()
plt.legend(handles = [z1,z2])
#plt.subplot(414)
#yaw1, = plt.plot(time_axis, [a['yaw']for a in est_pos], label = "estimated yaw")
#yaw2, = plt.plot(time_axis, 180/np.pi *testData[:,6], label = "Measured yaw")
#plt.grid()
#plt.legend(handles = [yaw1,yaw2])

plt.show()