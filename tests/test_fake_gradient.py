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

# In this project, we'll create a fake gradient.
gradient = Object(
    master=display,
    origin=Coord(0, 0),
    id="gradient"
)

for x in range(0, 51):
    segment = Segment(
        origin=Coord(x/10, 0),
        end=Coord(x/10, 1),
        specs={"color": f"#{round(x*5.1):02x}0000", "width": 3}
    )
    gradient.add_shape(segment)
display.add_object("gradient", gradient) # Finally, we add the gradient to the display.

fps = 60
while True:
    engine.draw_frame()
    time.sleep(1 / fps)

# This looks very good! Gradients coming by or in Vispen v2.0!