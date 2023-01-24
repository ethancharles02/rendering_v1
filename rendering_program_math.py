#allows the program to have a rotated camera
#add to the current math that will allow efficient manipulation of objects
from math import *

#testing
import time

class ray:
    """
    editable variables:
        ray_origin = (float, float, float), def = (0, 0, 0)
        ray_direction = (float, float), def = (0, 0)
            ray_direction should be expressed in degrees
            the def of (0, 0) would be an x axis ray while (90, 0) is the y axis; (0, 90) would be z axis
  
    functions:
        rayLenPos(self, length)
            finds the endpoint position of a ray based on a given length for that ray
            returns in a list format of (x, y, z)
      
        pointFromX(self, x)
          gives the full coordinate point of the x version of that ray
      
        pointFromY(self, y)
          gives the full coordinate point of the y version of that ray
      
        pointFromZ(self, z)
          gives the full coordinate point of the z version of that ray
      
    """
    def rayLenPos(self, length):
        """
        Returns the coordinate points in a list of x,y,z format based on the given length
        """
        x = length * cos(radians(self.ray_direction[1])) * cos(radians(self.ray_direction[0])) + self.ray_origin[0]
        y = length * cos(radians(self.ray_direction[1])) * sin(radians(self.ray_direction[0])) + self.ray_origin[1]
        z = length * sin(radians(self.ray_direction[1])) + self.ray_origin[2]
        return (x, y, z)
    
    def __init__(self, ray_origin = (0.0, 0.0, 0.0), ray_direction = (0.0, 0.0)):
        self.ray_origin = ray_origin
        self.ray_direction = ray_direction
        self.endPoint = self.rayLenPos(1500)
        #finish setting up all axisAlignment variables
        #if (self.ray_direction[0] == 0 and self.ray_direction[1] == 0) or (self.ray_direction[0] == 180 and self.ray_direction[1] == 0):
        #  self.axisAlignment = "x"
        #if (self.ray_direction[0] == 90 and self.ray_direction[1] == 0) or (self.ray_direction[0] == 270 and self.ray_direction[1] == 0):
        #  self.axisAlignment = "y"
        #if (self.ray_direction[0] == 0 and self.ray_direction[1] == 0) or (self.ray_direction[0] ==  and self.ray_direction[1] == 180):
        #  self.axisAlignment = "z"
    pass

    def pointFromX(self, x): 
        return(x, (x - self.ray_origin[0])*tan(radians(self.ray_direction[0])) + self.ray_origin[1], (x - self.ray_origin[0])*tan(radians(self.ray_direction[1]))/cos(radians(self.ray_direction[0])) + self.ray_origin[2])

    def pointFromY(self, y): 
        return((y - self.ray_origin[1])/tan(radians(self.ray_direction[0])) + self.ray_origin[0], y, (y - self.ray_origin[1])*tan(radians(self.ray_direction[1]))/sin(radians(self.ray_direction[0])) + self.ray_origin[2])

    def pointFromZ(self, z): 
        return(cos(radians(self.ray_direction[0]))*(z - self.ray_origin[2])/tan(radians(self.ray_direction[1])) + self.ray_origin[0], sin(radians(self.ray_direction[0]))*(z - self.ray_origin[2])/tan(radians(self.ray_direction[1])) + self.ray_origin[1], z)



class recPrism:
    """
    editable variables:
        length = float, def = 1, length refers to the x variable
        width = float, def = 1, width refers to the y variable
        height = float, def = 1, height refers to the z variable
        origin = (float, float, float), def = (0, 0, 0)
        rotation = (float, float), def = (0, 0), 1st point is the xy rotation while the second is the z rotation

    callable variables:
        (all current editable variables)

        corners[1-8][0-2] (
          arg 1 refers to corner number; 1 being farthest top left with 8 being closest bottom right
          arg 2 refers to the coordinate; 0 being x, 2 being z
        )

        longestdist (refers to the longest possible distance on that object)

        plane
          calls a dictionary with references:
            "x" : (lesser side plane, higher side plane)
            "y" : (lesser side plane, higher side plane)
            "z" : (lesser side plane, higher side plane)
    """
    def __init__(self, length = 1, width = 1, height = 1, origin = (0, 0, 0)):
        self.length = length
        self.width = width
        self.height = height
        self.origin = origin
        
        self.corners = {
            1 : (self.origin[0] - self.length/2, self.origin[1] + self.width/2, self.origin[2] + self.height/2),
            2 : (self.origin[0] + self.length/2, self.origin[1] + self.width/2, self.origin[2] + self.height/2),
            3 : (self.origin[0] - self.length/2, self.origin[1] - self.width/2, self.origin[2] + self.height/2),
            4 : (self.origin[0] + self.length/2, self.origin[1] - self.width/2, self.origin[2] + self.height/2),
            5 : (self.origin[0] - self.length/2, self.origin[1] + self.width/2, self.origin[2] - self.height/2),
            6 : (self.origin[0] + self.length/2, self.origin[1] + self.width/2, self.origin[2] - self.height/2),
            7 : (self.origin[0] - self.length/2, self.origin[1] - self.width/2, self.origin[2] - self.height/2),
            8 : (self.origin[0] + self.length/2, self.origin[1] - self.width/2, self.origin[2] - self.height/2),
            }
          
        self.longestdist = (
            (self.corners[8][0] - self.corners[1][0]) ** 2 + 
            (self.corners[8][1] - self.corners[1][1]) ** 2 +
            (self.corners[8][2] - self.corners[1][2]) ** 2
            ) ** (1/2)
          
        self.plane = {
            "x" : (self.origin[0] - self.length / 2, self.origin[0] + self.length / 2),
            "y" : (self.origin[1] - self.width / 2, self.origin[1] + self.width / 2),
            "z" : (self.origin[2] - self.height / 2, self.origin[2] + self.height / 2)
            }

    def updatePosData(self):
        self.corners = {
            1 : (self.origin[0] - self.length/2, self.origin[1] + self.width/2, self.origin[2] + self.height/2),
            2 : (self.origin[0] + self.length/2, self.origin[1] + self.width/2, self.origin[2] + self.height/2),
            3 : (self.origin[0] - self.length/2, self.origin[1] - self.width/2, self.origin[2] + self.height/2),
            4 : (self.origin[0] + self.length/2, self.origin[1] - self.width/2, self.origin[2] + self.height/2),
            5 : (self.origin[0] - self.length/2, self.origin[1] + self.width/2, self.origin[2] - self.height/2),
            6 : (self.origin[0] + self.length/2, self.origin[1] + self.width/2, self.origin[2] - self.height/2),
            7 : (self.origin[0] - self.length/2, self.origin[1] - self.width/2, self.origin[2] - self.height/2),
            8 : (self.origin[0] + self.length/2, self.origin[1] - self.width/2, self.origin[2] - self.height/2),
            }
          
        self.longestdist = (
            (self.corners[8][0] - self.corners[1][0]) ** 2 + 
            (self.corners[8][1] - self.corners[1][1]) ** 2 +
            (self.corners[8][2] - self.corners[1][2]) ** 2
            ) ** (1/2)
          
        self.plane = {
            "x" : (self.origin[0] - self.length / 2, self.origin[0] + self.length / 2),
            "y" : (self.origin[1] - self.width / 2, self.origin[1] + self.width / 2),
            "z" : (self.origin[2] - self.height / 2, self.origin[2] + self.height / 2)
            }



def betweenPlanes(point):
    """
    Checks if the point given is between the 2 planes given
    betweenPlanes(point)
    ie. betweenPlanes(0) would check the coords of the temporary point tempColPoint between the y and z planes assuming that that the number given corresponds to the point on the plane. 0 = x, 1 = y, 2 = z
    """
    if point == 0:
        if (gRecPrism.plane["y"][0] <= tempColPoint[1] <= gRecPrism.plane["y"][1]) and (gRecPrism.plane["z"][0] <= tempColPoint[2] <= gRecPrism.plane["z"][1]):
            return(True)
        else:
            return(False)
    elif point == 1:
        if (gRecPrism.plane["x"][0] <= tempColPoint[0] <= gRecPrism.plane["x"][1]) and (gRecPrism.plane["z"][0] <= tempColPoint[2] <= gRecPrism.plane["z"][1]):
            return(True)
        else:
            return(False)
    else:
        if (gRecPrism.plane["x"][0] <= tempColPoint[0] <= gRecPrism.plane["x"][1]) and (gRecPrism.plane["y"][0] <= tempColPoint[1] <= gRecPrism.plane["y"][1]):
            return(True)
        else:
            return(False)

def distPoints(p1, p2):
    """
    takes the two 3d points and finds the distance between them assuming that the points are given in the form (x, y, z)
    """
    return((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2) ** (1/2)

def showCollisionPoints(gRay, gRecPrism):
    """
    returns the distance if the given ray and given rectangular prism have collision points
    showCollisionPoints(gRay, gRecPrism) gRay refers to the given ray class that you want to check the collision for
                                         gRecPrism refers to the recPrism class given
    """
    #changed the return arguments from showing the distance to showing a singular color based on what side the collision is on
    #x collision checking
    #optimization options: only do math if the first angle points in the direction of the cube
    if gRay.ray_origin[0] <= gRecPrism.plane["x"][0]:
        if (gRay.endPoint[0] < gRecPrism.plane["x"][0]) != (gRay.ray_origin[0] < gRecPrism.plane["x"][0]):
            tempColPoint = gRay.pointFromX(gRecPrism.plane["x"][0])
            if (gRecPrism.plane["y"][0] <= tempColPoint[1] <= gRecPrism.plane["y"][1]) and (gRecPrism.plane["z"][0] <= tempColPoint[2] <= gRecPrism.plane["z"][1]):
                return((255,0,0))
      
    if gRay.ray_origin[0] >= gRecPrism.plane["x"][1]:
        if (gRay.endPoint[0] < gRecPrism.plane["x"][1]) != (gRay.ray_origin[0] < gRecPrism.plane["x"][1]):
            tempColPoint = gRay.pointFromX(gRecPrism.plane["x"][1])
            if (gRecPrism.plane["y"][0] <= tempColPoint[1] <= gRecPrism.plane["y"][1]) and (gRecPrism.plane["z"][0] <= tempColPoint[2] <= gRecPrism.plane["z"][1]):
                return((255,255,0))
      
    #y collision checking
    if gRay.ray_origin[1] <= gRecPrism.plane["y"][0]:
        if (gRay.endPoint[1] < gRecPrism.plane["y"][0]) != (gRay.ray_origin[1] < gRecPrism.plane["y"][0]):
            tempColPoint = gRay.pointFromY(gRecPrism.plane["y"][0])
            if (gRecPrism.plane["x"][0] <= tempColPoint[0] <= gRecPrism.plane["x"][1]) and (gRecPrism.plane["z"][0] <= tempColPoint[2] <= gRecPrism.plane["z"][1]):
                return((255,0,255))
      
    if gRay.ray_origin[1] >= gRecPrism.plane["y"][1]:
        if (gRay.endPoint[1] < gRecPrism.plane["y"][1]) != (gRay.ray_origin[1] < gRecPrism.plane["y"][1]):
            tempColPoint = gRay.pointFromY(gRecPrism.plane["y"][1])
            if (gRecPrism.plane["x"][0] <= tempColPoint[0] <= gRecPrism.plane["x"][1]) and (gRecPrism.plane["z"][0] <= tempColPoint[2] <= gRecPrism.plane["z"][1]):
                return((0,255,0))
      
    #z collision checking
    if gRay.ray_origin[2] <= gRecPrism.plane["z"][0]:
        if (gRay.endPoint[2] < gRecPrism.plane["z"][0]) != (gRay.ray_origin[2] < gRecPrism.plane["z"][0]):
            tempColPoint = gRay.pointFromZ(gRecPrism.plane["z"][0])
            if (gRecPrism.plane["x"][0] <= tempColPoint[0] <= gRecPrism.plane["x"][1]) and (gRecPrism.plane["y"][0] <= tempColPoint[1] <= gRecPrism.plane["y"][1]):
                return((0,255,255))

    if gRay.ray_origin[2] >= gRecPrism.plane["z"][1]:
        if (gRay.endPoint[2] < gRecPrism.plane["z"][1]) != (gRay.ray_origin[2] < gRecPrism.plane["z"][1]):
            tempColPoint = gRay.pointFromZ(gRecPrism.plane["z"][1])
            if (gRecPrism.plane["x"][0] <= tempColPoint[0] <= gRecPrism.plane["x"][1]) and (gRecPrism.plane["y"][0] <= tempColPoint[1] <= gRecPrism.plane["y"][1]):
                return((0,0,255))
    else:
        return(False)

def angleBetween(p1, p2):
    theta = atan2((p2[1] - p1[1]), (p2[0] - p1[0]))
    phi = degrees(atan2((p2[2] - p1[2]), (((p2[1] - p1[1]) / sin(theta)))))
    return(degrees(theta) % 360, phi % 360)
  
class camera:
    """
    
    """
    def __init__(self, fov = 100, origin = (0, 0, 0), direction = (90, 0), canvas_width = 10, canvas_height = 10):
        self.fov = fov
        self.origin = origin
        self.direction = direction
        
        left_coords = ray(ray_origin = (self.origin[0], self.origin[1] + 1, self.origin[2]), ray_direction = (self.direction[0] + self.fov/2, 0)).rayLenPos(1)
        x = left_coords[0]
        y = left_coords[1]
        z = left_coords[0] * -1
        
        cube_start_pos = (x, y, z)
        x_change = 2 * x / canvas_height
        z_change = 2 * z / canvas_height
        
        self.camera_rays = []
        self.camera_angle_list_theta = []
        self.camera_angle_list_phi = []
        self.camera_angle_list = []
        i = 0
        for x in range(canvas_width):
            for z in range(canvas_height):
                self.camera_rays.append(ray(ray_origin = self.origin, ray_direction = angleBetween(self.origin, (cube_start_pos[0] - x * x_change * (canvas_width + 1) / canvas_width, cube_start_pos[1], cube_start_pos[2] - z * z_change * (canvas_height + 1) / canvas_height))))
                self.camera_angle_list_theta.append(self.camera_rays[i].ray_direction[0])
                self.camera_angle_list_phi.append(self.camera_rays[i].ray_direction[1])
                self.camera_angle_list.append((self.camera_angle_list_theta[i], self.camera_angle_list_phi[i]))
                i += 1
    
def convertCoordToScreenCoord(camera, coord = (0,0,0)):
    cameraAngleToCoord = angleBetween(camera.origin, coord)
    return cameraAngleToCoord

def bbox(camera, cube, canvas_width, canvas_height):
    """
    """
    
    angleCameraList = camera.camera_angle_list
    
    #print(angleCameraList)
    
    for iteration in range(8):
        #finds the angle between the camera and the iterations corner
        angleCubeOrig = angleBetween(camera.origin, cube.corners[iteration + 1])

        angleCheckRangeX = [0, canvas_width - 1]
        while angleCameraList[angleCheckRangeX[0] * canvas_height][0] != angleCameraList[(angleCheckRangeX[1] - 1) * canvas_height][0]:
            if angleCameraList[angleCheckRangeX[0] * canvas_height][0] > angleCubeOrig[0] > angleCameraList[((angleCheckRangeX[1] * canvas_height - angleCheckRangeX[0] * canvas_height) // 2) + angleCheckRangeX[0] * canvas_height][0]:
                angleCheckRangeX = [angleCheckRangeX[0], ((angleCheckRangeX[1] - angleCheckRangeX[0]) // 2) + angleCheckRangeX[0]]
                
            elif angleCameraList[((angleCheckRangeX[1] * canvas_height - angleCheckRangeX[0] * canvas_height) // 2) + angleCheckRangeX[0] * canvas_height][0] > angleCubeOrig[0] > angleCameraList[angleCheckRangeX[1] * canvas_height][0]:
                angleCheckRangeX = [((angleCheckRangeX[1] - angleCheckRangeX[0]) // 2) + angleCheckRangeX[0], angleCheckRangeX[1]]
            
            else:
                break
                        
        angleCheckRange = [angleCheckRangeX[0] * canvas_height, angleCheckRangeX[0] * canvas_height + canvas_height]
        
        optimizedAngleList = angleCameraList[angleCheckRange[0]:angleCheckRange[1]]
        
        while angleCameraList[angleCheckRange[0]][1] != angleCameraList[angleCheckRange[1] - 1][1]:
            if angleCameraList[angleCheckRange[0]][1] > angleCubeOrig[1] > angleCameraList[((angleCheckRange[1] - angleCheckRange[0]) // 2) + angleCheckRange[0]][1]:
                angleCheckRange = [angleCheckRange[0], ((angleCheckRange[1] - angleCheckRange[0]) // 2) + angleCheckRange[0]]
                
            elif angleCameraList[((angleCheckRange[1] - angleCheckRange[0]) // 2) + angleCheckRange[0]][1] > angleCubeOrig[1] > angleCameraList[angleCheckRange[1]][1]:
                angleCheckRange = [((angleCheckRange[1] - angleCheckRange[0]) // 2) + angleCheckRange[0], angleCheckRange[1]]
                
            else:
                break

        #the shortest distance in the list is the pixel that is closest to the corner of that cube
        pixelIndex = angleCheckRange[0]
        
        #converts the index into a coordinate on the actual screen
        pixelIndexCoords = [pixelIndex // canvas_height, pixelIndex % canvas_width]
        
        #rest of the code finds the bounding box that contains all of the cube in the smallest area
        if iteration == 0:
            bboxUpLeft = [pixelIndexCoords[0], pixelIndexCoords[1]]
            bboxBotRight = [pixelIndexCoords[0], pixelIndexCoords[1]]
            
        else:
            if pixelIndexCoords[0] < bboxUpLeft[0]:
                bboxUpLeft[0] = pixelIndexCoords[0]
                
            if pixelIndexCoords[0] > bboxBotRight[0]:
                bboxBotRight[0] = pixelIndexCoords[0]
                
            if pixelIndexCoords[1] < bboxUpLeft[1]:
                bboxUpLeft[1] = pixelIndexCoords[1]
                
            if pixelIndexCoords[1] > bboxBotRight[1]:
                bboxBotRight[1] = pixelIndexCoords[1]

    return(bboxUpLeft, bboxBotRight)