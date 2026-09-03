import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from vispen.vizwiz import (
    Engine,
    VizWiz,
    Display,
    Object,
    Coord,
    Segment
)

engine = Engine() # First step, creating the engine
vizwiz = VizWiz() # Next, we create the VizWiz
engine.viz = vizwiz
display = Display(
    master=engine.viz,
    origin=Coord(0, 0),
    top_right=Coord(400, 300),
    id="main",
    scale=20
) # This is how you create the display.
vizwiz.add_display(display)

# In this project, we'll draw a bunch of segments! So, we'll create a grid object.
grid = Object(
    master=display,
    origin=Coord(0, 0),
    id="grid"
)
# First, we'll draw the vertical segments.
for x in range(0, 21):
    segment = Segment(
        origin=Coord(x, 0),
        end=Coord(x, 15),
        specs={"color":"black", "width":1}
    )
    grid.add_shape(segment)
# Next, we'll draw the horizontal segments.
for y in range(0, 16):
    segment = Segment(
        origin=Coord(0, y),
        end=Coord(20, y),
        specs={"color":"black", "width":1}
    )
    grid.add_shape(segment)
display.add_object("grid", grid) # Finally, we add the grid to the display.

# Time for the engine loop!
fps = 60
while True:
    engine.draw_frame()
    time.sleep(1 / fps)