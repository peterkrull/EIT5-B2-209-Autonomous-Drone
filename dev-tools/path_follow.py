import math,csv
import time

class PathFollow:
    def __init__(self, radiusUpdate, pathFileLocation) -> None:
        """
        Making pathFolow object

        Args:
            radius update (int)     : Radius to point before heading to next point
            patFileLocation (str)   : Location of path file
        """
        self.radiusUpdate = radiusUpdate    #Distance where next ref is taken
        self.path = 0                       #The Path. 
        self.count = 0                      #The step the drone heading for in at in path
        self.pathFileLocation = pathFileLocation
        self.loadPath()
        self.timeStamped = False
        self.clockReachedDest = 0

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
        distPosToRef = math.sqrt((float(self.path[self.count][0]) - position[1])**2 + (
            float(self.path[self.count][1]) - position[2])**2 + (float(self.path[self.count][2]) - position[3])**2)
        print("SP",self.path[self.count])
        print("CO",position[1],position[2],position[3])
        print("DS",distPosToRef)
        
        # Ensure hover time at all points
        if(distPosToRef < self.radiusUpdate):     #If inside update radius
            # Remove comments to hold positions before flying
            if(self.timeStamped == False):
                self.timeStamped = True
                self.clockReachedDest = time.monotonic()
            
            if(time.monotonic() - self.clockReachedDest >= float(self.path[self.count][4])):
                self.timeStamped = False
                self.count +=1

        #
        if self.count < len(self.path):
            return {"x":float(self.path[self.count][0]),
                    "y":float(self.path[self.count][1]),
                    "z":float(self.path[self.count][2]),
                    "yaw":float(self.path[self.count][3]),
                    "holdTime":float(self.path[self.count][4]),
                    "viconAvailable":float(self.path[self.count][5])} 
        else: raise IndexError("End of flight file has been reached, handle this accordingly.")