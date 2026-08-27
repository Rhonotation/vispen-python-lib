if __name__ == "__main__":
    import sys
    import os
    import time

    # Make src/ visible to Python
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

    from vispen.vizwiz import (
        Engine,
        Display,
        Object,
        Coord,
        Rect,
        TanhTween
    )

    engine = Engine()

    display = Display(
        master=engine.viz,
        origin=Coord(-200, -150),
        top_right=Coord(200, 150),
        id="main",
        scale=20
    )

    engine.add_display("main", display)

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

    display.objects["box1"] = obj1
    display.objects["box2"] = obj2

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

    while True:
        engine.draw_frame()
        time.sleep(1/60)