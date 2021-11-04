import threading
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie

# Library for data logging
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger
import logging
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

#Data logging thread
class myThread1 (threading.Thread):
   def __init__(self, URI = None):
      threading.Thread.__init__(self)
      self.URI = 'radio://0/80/2M' if not URI else URI
      cflib.crtp.init_drivers()
      logging.basicConfig(level=logging.ERROR)
      self.cf = Crazyflie()
   def run(self):
      lg_stab = LogConfig(name='category', period_in_ms=10)
      #lg_stab.add_variable('motor.m1', 'uint8_t')
      #lg_stab.add_variable('motor.m2', 'uint8_t')
      #lg_stab.add_variable('motor.m3', 'uint8_t')
      #lg_stab.add_variable('motor.m4', 'uint8_t')
      lg_stab.add_variable('stabilizer.roll', 'float')
      lg_stab.add_variable('baro.temp', 'float')
      #lg_stab.add_variable('kalman.varZ', 'float')
      data1 = []

      with SyncCrazyflie(self.URI, cf=Crazyflie(rw_cache='./cache')) as scf:
         with SyncLogger(scf, lg_stab) as logger:
            for log_entry in logger:
               data1.append(log_entry[1])
               print(data1[len(data1)-1])
         return data1[len(data1)-1]

#Thread der simulere drone_main
class myThread2 (threading.Thread):
   def __init__(self, delay):
      threading.Thread.__init__(self)
      self.delay = delay
   def run(self):
      while True:
         print("ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
         time.sleep(self.delay)



# Create new threads
thread1 = myThread1()
thread2 = myThread2(0.003)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")
