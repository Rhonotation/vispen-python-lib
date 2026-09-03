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
    TanhTween
)

if __name__ == "__main__":
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

    # 4. Create objects
    obj1 = Object(
        master=display,
        origin=Coord(0, 0),
        id="box1",
        shapes=[Rect(Coord(0, 0), Coord(2, 2))]
    )

    obj2 = Object(
        master=display,
        origin=Coord(5, 0),
        id="box2",
        shapes=[Rect(Coord(0, 0), Coord(1, 3))]
    )

    # 5. Add objects to the display
    display.add_object("box1", obj1)
    display.add_object("box2", obj2)

    # 6. Add tweens
    start_time = time.time()

    display.add_tween(
        "box1",
        TanhTween(
            start=start_time,
            duration=3,
            point1=Coord(0, 0),
            point2=Coord(10, 10),
            sharpness=3
        )
    )

    display.add_tween(
        "box2",
        TanhTween(
            start=start_time,
            duration=5,
            point1=Coord(5, 0),
            point2=Coord(-5, 10),
            sharpness=4
        )
    )

    # 7. Run the engine loop
    fps = 60
    while True:
        engine.draw_frame()
        time.sleep(1 / fps)
