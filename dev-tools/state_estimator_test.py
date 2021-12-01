from state_estimator import state_estimator
import csv
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from scipy.fft import fft, fftfreq
from scipy import signal


#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\test-of-barometer\\1637152127_baro_meas.csv'
#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\onboard-sensor-drift\\1637063677_test_flyvning.csv'
#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\onboard-sensor-drift\\1637829739_track_flight.csv'
#file = 'C:\\Users\\bosto\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\test-results\\flowdeck-measurements\\1637841045_højde2_3.csv'
file ='C:\\Users\\bosto\\Downloads\\1638195978_y_step_flowdeck.csv'
#file ='C:\\Users\\bosto\\Downloads\\1638197639_x_step_flowdeck.csv'
with open(file, newline='') as csvFile:
    dataReader = csv.DictReader(csvFile, delimiter=",")
    testDataHeader = dataReader.fieldnames
    testData = list(csv.reader(csvFile,delimiter=","))
    testData = [x for x in testData if '' not in x]
    testData = np.array(testData).astype(np.float)

#[række,søjle]

pos = {'x':testData[0][1], 'y': testData[0][2], 'z': testData[0][3], 'yaw': testData[0][6]}
viconInit = [testData[0][0]-0.01, testData[0][1], testData[0][2], testData[0][3], testData[0][4], testData[0][5],testData[0][6]]
state_est = state_estimator(pos, viconInit, flowdeck=True, log = True)


gx_index = testDataHeader.index("gyro_x")
gy_index = testDataHeader.index("gyro_y")
ax_index = testDataHeader.index("acc_x")
ay_index = testDataHeader.index("acc_y")
az_index = testDataHeader.index("acc_z")
seYaw_index = testDataHeader.index("stateEstimate_yaw")
#baro_index = testDataHeader.index("baro_pressure")
se_vc_index = testDataHeader.index("stateEstimate_vz")
se_ac_index = testDataHeader.index("stateEstimate_az")
fx_index = testDataHeader.index("motion_deltaX")
fy_index = testDataHeader.index("motion_deltaY")
fz_index = testDataHeader.index("range_zrange")


est_pos = []
time_axis = []
vicon_available = 1
for i in testData:
    vicon_pos = []
    for j in range(7):
        vicon_pos.append(i[j])
    
    if vicon_available == 1:
        lotto_viconAvailable = random.randrange(0,500,1)
        #if lotto_viconAvailable == 69 and i[0]>5:
        if i[0]>0:
            vicon_available = 0
            print("switch time:", i[0])

    #print(vicon_pos)
    drone_data = {'gyro.x':i[gx_index], 'gyro.y':i[gy_index], 'acc.x':i[ax_index], 'acc.y':i[ay_index], 'acc.z':i[az_index], 'stateEstimate.yaw':i[seYaw_index],'time':i[0], 'stateEstimate.vz':i[se_vc_index], 'stateEstimate.az':i[se_ac_index], 'motion.deltaY':i[fy_index], 'motion.deltaX':i[fx_index], 'range.zrange':i[fz_index] } 

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
plt.legend(handles = [x1,x2], loc = 'lower right')
ax = plt.gca()
ax.set_ylim([-3000,3000])
plt.subplot(312)
y1, = plt.plot(time_axis, [a['y']for a in est_pos], label = "estimated y")
y2, = plt.plot(time_axis, testData[:,2], label = "Measured y")
plt.grid()
#plt.legend(handles = [y1,y2], loc = 'lower right')
ax = plt.gca()
ax.set_ylim([-3000,3000])
plt.subplot(313)
z1, = plt.plot(time_axis, [a['z']for a in est_pos], label = "estimated z")
z2, = plt.plot(time_axis, testData[:,3], label = "Measured z")
plt.grid()
plt.legend(handles = [z1,z2], loc = 'lower right')


plt.figure(2)
plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_fd_vel['x'])






#plt.subplot(414)
#yaw1, = plt.plot(time_axis, [a['yaw']for a in est_pos], label = "estimated yaw")
#yaw2, = plt.plot(time_axis, 180/np.pi *testData[:,6], label = "Measured yaw")
#plt.grid()
#plt.legend(handles = [yaw1,yaw2])

#plt.figure(2)

#x1, = plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_body_vel['x'], label = 'bodyframe vel')
#x2, = plt.plot(state_est.xy_estimator.log_time[0:len(state_est.xy_estimator.log_vicon_vel['x'])], state_est.xy_estimator.log_vicon_vel['x'], label = 'vicon velocity, body')
#x3, = plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_fd_vel_filtered['x'], label = 'flow deck vel filtered')
#x4, = plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_ga_vel['x'])
#plt.legend(handles = [x1, x2, x3], loc = 'lower right')
#plt.grid()
#plt.title('x velocity')


#plt.figure(4)

#x1, = plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_body_vel['y'], label = 'bodyframe vel')
#x2, = plt.plot(state_est.xy_estimator.log_time[0:len(state_est.xy_estimator.log_vicon_vel['y'])], state_est.xy_estimator.log_vicon_vel['y'], label = 'vicon velocity, body')
#x3, = plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_fd_vel_filtered['y'], label = 'flow deck vel filtered')
#x4, = plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_ga_vel['x'])
#plt.legend(handles = [x1, x2, x3], loc = 'lower right')
#plt.grid()
#plt.title('y velocity')


#N  =len([a['y']for a in est_pos])
#T  = .015
#X  = np.linspace(0,N*T, endpoint=False)
#yf = fft([a['y']for a in est_pos]*np.hamming(N))
#print(state_est.xy_estimator.log_body_vel['x'])
#print(yf)
#xf  =fftfreq(N,d = T)[:N//2]

#plt.figure(3)
#plt.semilogx(xf, 2/N*np.abs(yf[0:N//2]))
#plt.grid()


#plt.figure(6)
#f, t, Zxx = signal.stft(state_est.xy_estimator.log_acc['pitch'], 1/T)
#plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
#plt.title('STFT Magnitude')
#plt.ylabel('Frequency [Hz]')
#plt.xlabel('Time [sec]')



#plt.figure(5)
#x1, = plt.plot(testData[:,0], testData[:,gy_index])
#plt.plot(state_est.xy_estimator.log_time, state_est.xy_estimator.log_acc['pitch'])
#plt.grid()
#plt.title('acceleration pitch')
#x2, = plt.plot(testData[:,1], acc_x)


plt.show()