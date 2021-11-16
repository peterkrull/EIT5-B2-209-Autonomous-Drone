import logging
import time
import csv
import numpy as np
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def simple_log(scf, logconf):
    totalData = []
    with SyncLogger(scf, lg_stab) as logger:
        startTime = time.time()
        for log_entry in logger:

            data = log_entry[1]
            dataTime = time.time()
            print( '%s' %(data))

            
            totalData.append([dataTime, data['gyro.x'],data['gyro.y'],data['gyro.z'],data['acc.x'],data['acc.y'],data['acc.z'],data['stateEstimate.yaw'],data['baro.pressure'],data['pm.vbat']])     
            if(time.time()>startTime+420):
                break
        
        with open(str(int(startTime))+"_"+"sensorDrift"+".csv",'w',newline='',encoding='UTF8') as file:
            totalData = np.array(totalData)
            writer = csv.writer(file)
            writer.writerows(totalData)
            
...

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('gyro.x', 'float')
    lg_stab.add_variable('gyro.y', 'float')
    lg_stab.add_variable('gyro.z', 'float')
    lg_stab.add_variable('acc.x', 'FP16')
    lg_stab.add_variable('acc.y', 'FP16')
    lg_stab.add_variable('acc.z', 'FP16')
    lg_stab.add_variable('stateEstimate.yaw', 'FP16')
    lg_stab.add_variable('baro.pressure', 'float')
    lg_stab.add_variable('pm.vbat', 'FP16')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_log(scf, lg_stab)