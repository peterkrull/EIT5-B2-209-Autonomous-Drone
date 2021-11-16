import matplotlib.pyplot as plt
import numpy as np

class path_visualizer:
    xValues = []
    yValues = []
    zValues = []
    def __init__(self, path):
        self.ax = plt.figure()
        self.ax = fig.add_subplot(projection='3d')
        self.ax.plot(path['x'],path['y'],path['z'])

        path = np.array(path).astype(np.float)
        pathX = path[:,0]
        pathY = path[:,1]
        pathZ = path[:,2]

        max_range = np.array([pathX.max()-pathX.min(), pathY.max()-pathY.min(), pathZ.max()-pathZ.min()]).max() / 2.0
        mid_x = (pathX.max()+pathX.min()) * 0.5
        mid_y = (pathY.max()+pathY.min()) * 0.5
        mid_z = (pathZ.max()+pathZ.min()) * 0.5
        axisBuffer = 500
        self.ax.set_xlim(mid_x - max_range -axisBuffer, mid_x + max_range+axisBuffer)
        self.ax.set_ylim(mid_y - max_range-axisBuffer, mid_y + max_range+axisBuffer)
        self.ax.set_zlim(mid_z - max_range-axisBuffer, mid_z + max_range+axisBuffer)

        plt.show()


    def updateFrame(self,coordinate):
        self.xValues.append(coordinate['x'])
        self.xValues.append(coordinate['y'])
        self.xValues.append(coordinate['z'])
        self.ax.plot(self.xValues,self.yValues,self.zValues, color='black')
        
        if len(self.xValues)>10:
            self.xValues.pop(0)
            self.yValues.pop(0)
            self.zValues.pop(0)
        
        plt.pause(.01)