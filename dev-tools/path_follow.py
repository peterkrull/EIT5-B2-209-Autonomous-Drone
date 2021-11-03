import math,csv

class PathFollow:
    def __init__(self, radiusUpdate, pathFileLocation) -> None:
        """
        Making path object

        Args:
            radius update (int)     : Radius to point before heading to next point
            patFileLocation (str)   : Location of path file
        """


        self.radiusUpdate = radiusUpdate    #Distance where next ref is taken
        self.path = 0                       #The Path. 
        self.count = 0                      #The step the drone heading for in at in path
        self.pathFileLocation = pathFileLocation
        self.loadPath()

    def loadPath(self):  # Path is csv file
        file = open(self.pathFileLocation)
        path = list(csv.reader(file, delimiter=","))
        self.path = path
        return path

    def getRef(self, position):  # Returning cordinate heading for point. Opdates when close to point
        """
        Returns refrence positions, including yaw

        Args:
            position (int) (x,y,z) : unit mm
        """

        # Beregn afstand mellem position of ref punkt.
        distPosToRef = math.sqrt((float(self.path[self.count][1]) - position[1])**2 + (
            float(self.path[self.count][2]) - position[2])**2 + (float(self.path[self.count][3]) - position[3])**2)
        
        if(distPosToRef < self.radiusUpdate):     #Hvis inden for radius til 
            self.count +=1          

        if not (self.count >= len(self.path)):
            return self.path[self.count]
       
        # return xRef, yRef, zRef, Yaw

# For Testing
# pathFollow = PathFollow(500,"dev-tools/Course_development/courseToFollow.csv") 
# print(pathFollow.getRef([5, 5, 5, 5]))
