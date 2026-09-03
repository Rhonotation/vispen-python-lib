import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from vispen.vizwiz import (
    Engine, Display, Object, Coord, Rect, TanhTween, Looper
)
from vispen.vizwiz import MultInterp

if __name__ == "__main__":
    engine = Engine()

    display = Display(
        master=engine.viz,
        origin=Coord(-200, -150),
        top_right=Coord(200, 150),
        id="main",
        scale=20
    )
    engine.add_display("main", display)

    box = Object(
        master=display,
        origin=Coord(0, 0),
        id="box",
        shapes=[Rect(Coord(0, 0), Coord(2, 2), specs={"fill_color": "blue", "color": "green", "width": 5})]
    )
    display.objects["box"] = box

    engine.viz.screen.tracer(0)

    # Let the engine initialize
    time.sleep(0.1)
    start = time.time()

    # Four tweens, no manual time offsets needed
    tweens = [
        TanhTween(start, 2, Coord(0, 0), Coord(10, 0), 3),
        TanhTween(start+2, 2, Coord(10, 0), Coord(10, 10), 3),
        TanhTween(start+4, 2, Coord(10, 10), Coord(0, 10), 3),
        TanhTween(start+6, 2, Coord(0, 10), Coord(0, 0), 3),
    ]

    # Your MultInterp runs them in order
    chain = Looper([MultInterp(tweens)])

    display.add_tween("box", chain)

    while True:
        engine.draw_frame()
        time.sleep(1/60)
