# https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
# the ray created between a position and the camera origin will intersect the theoretical box that is the screen. find that intersection point, convert it to a relative point on the theoretical box, floor divide and modulos it into the actual screen coord
# create rectangles for the parts of the screen that aren't rendering the cube
# implement controls for moving the camera
# implement the testing for finding the closest tuple point from a list found in testing.py in order to find the closest pixel for the angle between the camera origin and the corner of the cube
# rendering_program_v3 - use the testing done in trinket and make a program that renders based on vertices
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from random import *
import tkinter
import time
import os
from rendering_program_math import *
from math import *

master = tkinter.Tk()

canvas_width = 500
canvas_height = 500
w = tkinter.Canvas(master, width=canvas_width, height=canvas_height)
w.pack()

im = Image.new('RGB', (canvas_width, canvas_height), (255,255,255))
px = im.load()

def clearFrame():
    global im
    im = Image.new('RGB', (canvas_width, canvas_height), (255,255,255))
    
def createFrame():
    global img
    global w
    img = ImageTk.PhotoImage(image=im, size=None)
    w.create_image(canvas_width/2,canvas_height/2,image=img)
    w.update()

def updateFPS():
    timeFromLastFrame = time.monotonic() - curTime
    FPS = timeFromLastFrame ** -1
    print(FPS)

camera1 = camera(fov = 100, origin = (0, -30, 0), direction = (90, 0), canvas_width = canvas_width, canvas_height = canvas_height)
cube1 = recPrism(origin = (0, 10, -12), length = 10, width = 10, height = 10)

#print(camera1.camera_angle_list)

if False:
    while True:
        curTime = time.monotonic()
        clearFrame()
        i = 0
        for x in range(canvas_width):
            for y in range(canvas_height):
                pointDist = showCollisionPoints(camera1.camera_rays[i], cube1)
                if(pointDist):
                    im.putpixel((x,y), (int((pointDist * 200) % 255), int((pointDist * 200) % 255), int((pointDist * 200) % 255)))
                else:
                    im.putpixel((x,y),(0,0,0))
                i += 1
        createFrame()
        updateFPS()

deg = 0

while True:
    curTime = time.monotonic()
    clearFrame()
    
    bboxCoords = bbox(camera1, cube1, canvas_width, canvas_height)
    #bboxCoords = ((0,0),(canvas_width - 1,canvas_height - 1))
    bboxUpLeft = bboxCoords[0]
    bboxBotRight = bboxCoords[1]

    print(bboxCoords)
    

    i = 0
    for x in range(canvas_width):
        for y in range(canvas_height):
            if x >= bboxUpLeft[0] and x <= bboxBotRight[0] and y >= bboxUpLeft[1] and y <= bboxBotRight[1]:
                pointDist = showCollisionPoints(camera1.camera_rays[i], cube1)
                if(pointDist):
                    im.putpixel((x,y), (pointDist))
                else:
                    im.putpixel((x,y),(0,0,0))
            else:
                im.putpixel((x,y),(0,0,0))
            i += 1
    
    im.putpixel(bboxUpLeft, (255, 255, 255))
    im.putpixel(bboxBotRight, (255, 255, 255))
    print(convertCoordToScreenCoord(camera1, cube1.corners[1]))

    cube1.origin = (cube1.origin[0] - cos(radians(deg)), cube1.origin[1], cube1.origin[2] + sin(radians(deg)))
    # cube1.origin = (cube1.origin[0], cube1.origin[1], cube1.origin[2] + 2)
    cube1.updatePosData()
    deg %= 360
    deg += 5
    #print(cube1.origin)
    createFrame()
    updateFPS()
    #time.sleep(100)