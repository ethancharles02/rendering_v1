## Overview
I made this back in high school. Mostly wanted to get an idea of what it takes to render basic shapes.
I plan to make a second version of this that can draw any number of shapes but doesn't follow the ray tracing method of rendering.
## Methods
This program renders a single cube in an inefficient yet interesting way:
* Creates a ray from the camera and searches along that path for an intersection with any of the cubes planes for every pixel on the screen
* For any intersection that it finds, it colors that pixel a given color
* By rendering this way, there are some fun things you can do with the colors, one of which is deciding the color based on the distance to that position
## TODO
* There is a bug with the optimization where it appears to be identifying the bounding box of the cube incorrectly, failing to draw it