import numpy as np

class PathFollow:
    def __init__(self, radiusUpdate, pathFileLocation) -> None:
        self.radiusUpdate = radiusUpdate    #Distance where next ref is taken
        self.path = 0                       #The Path. 
        self.count = 0                      #The step the drone heading for in at in path
        self.pathFileLocation = pathFileLocation
        self.loadPath()

    def loadPath(self):  # Path is csv file
        try:
            file = open(self.pathFileLocation)
            path = np.loadtxt(file, delimiter=",")
        except:
            print("Load Path failed")
            path = 0
        self.path = path
        return path

    def getRef(self, position):  # Returning cordinate heading for point. Opdates when close to point
        #Position format x,y,z, yaw. unit: mm
        # !!!! SO FAR YAW = 0!!!!!
      
        # Beregn afstand mellem position of ref punkt.
        distPosToRef = np.sqrt((self.path[self.count][1] - position[1])**2 + (
            self.path[self.count][2] - position[2])**2 + (self.path[self.count][3] - position[3])**2)
        
        if(distPosToRef < self.radiusUpdate):     #Hvis inden for radius til 
            self.count +=1          

        if not (self.count >= len(self.path)):
            return self.path[self.count]
       
        # return xRef, yRef, zRef, Yaw

#For Testing
#pathFollow = PathFollow(500,"C:\\Users\\laula\\Documents\\GitHub\\EIT5-B2-209-Autonomous-Drone\\simulations\\pathFollowing\\pathToFollow.csv") 
#print(pathFollow.getRef([5, 5, 5, 5]))
