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
    Rect,
    TanhTween,
    Looper,
    MultInterp
)


# 1. Create the engine
engine = Engine()

# 2. Create VizWiz explicitly (required in v1.1.2b)
viz = VizWiz()
engine.viz = viz

# 3. Create the display and add it to VizWiz
display = Display(
    master=viz,
    origin=Coord(-200, -150),
    top_right=Coord(200, 150),
    id="main",
    scale=20
)
viz.add_display(display)

# 4. Create the box object
box = Object(
    master=display,
    origin=Coord(0, 0),
    id="box",
    shapes=[
        Rect(
            origin=Coord(0, 0),
            top_right=Coord(2, 2),
            specs={"fill_color": "blue", "color": "green", "width": 5}
        )
    ]
)
display.add_object("box", box)

# 5. Let VizWiz initialize
time.sleep(0.1)
start = time.time()

# 6. Create the four tweens for the square path
tweens = [
    TanhTween(start,     2, Coord(0, 0),  Coord(10, 0),  3),
    TanhTween(start + 2, 2, Coord(10, 0), Coord(10, 10), 3),
    TanhTween(start + 4, 2, Coord(10, 10), Coord(0, 10),  3),
    TanhTween(start + 6, 2, Coord(0, 10),  Coord(0, 0),   3),
]

# 7. Wrap them in a looping chain
chain = Looper([MultInterp(tweens)])

# 8. Add tween to display
display.add_tween("box", chain)

# 9. Run the engine loop
fps = 60
while True:
    engine.draw_frame()
    time.sleep(1 / fps)