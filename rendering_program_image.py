#https://pillow.readthedocs.io/en/3.1.x/reference/Image.html
from PIL import Image
from PIL import ImageTk
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

# the cube has a texture representative of the distance from the camera to each point rendered on the cube, if this is used, change the corresponding math function to true
if False:
    deg = 0
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
        cube1 = recPrism(origin = (cube1.origin[0] + cos(radians(deg)), cube1.origin[1], cube1.origin[2] + sin(radians(deg))), length = 10, width = 10, height = 10)
        deg += 5
        createFrame()
        updateFPS()

# displays the cubes planes as solid textures, make sure the corresponding function is true if this one is used
if True:
    deg = 0

    while True:
        curTime = time.monotonic()
        clearFrame()
        i = 0
        for x in range(canvas_width):
            for y in range(canvas_height):
                pointDist = showCollisionPoints(camera1.camera_rays[i], cube1)
                if(pointDist):
                    im.putpixel((x,y), (pointDist))
                else:
                    im.putpixel((x,y),(0,0,0))
                i += 1
                #print((x,y),pointDist)
        cube1 = recPrism(origin = (cube1.origin[0] + cos(radians(deg)), cube1.origin[1], cube1.origin[2] + sin(radians(deg))), length = 10, width = 10, height = 10)
        deg += 5
        #print(cube1.origin)
        createFrame()
        updateFPS()
