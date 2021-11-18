from _typeshed import Self
from pitchRoll_estimator import pitchRoll_estimator

class state_estimator:
    def __init__(self, init_pos):
        self.est_pos = {'x','y','z','yaw'}
        self.xy_estimator = pitchRoll_estimator(init_pos)
        self.pos = {'x','y','z','yaw'}


        gyro_data = {'x' : drone_data['gyro_x'], 'y' : drone_data['gyro_y'], 'z' : drone_data['gyro_z']}
        acc_data = {'x': drone_data['acc_x'], 'y': drone_data['acc_y'], 'z': drone_data['acc_z']}

        #state estimation missing z
        self.est_pos['yaw'] = drone_data['stateEstimate_yaw']
        self.est_pos['x','y'] = self.xy_estimator.update(gyro_data, acc_data,self.pos['yaw'],drone_data['time'])
        self.est_pos['z'] = vicon_data['z'] #update pos using z-estimator
        
        if vicon_available == 1:
            #use vicon to acquire actual position to improve positioning of data.
            pass
        
        return self.est_pos

