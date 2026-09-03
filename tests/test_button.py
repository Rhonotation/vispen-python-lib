import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from vispen.vizwiz import (
    Engine, VizWiz, Display, Object, Coord, Rect, Hitbox, HitboxRect, Text
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

button = Object(
    master=display,
    origin=Coord(9,6.5),
    id="button"
) # We create a button object. Now it's time to give it its shape.

button_body = Rect(
    origin=Coord(0, 0),
    top_right=Coord(2, 2),
    specs={
        "fill_color":"pink",
        "color":"purple",
        "width":3
        }
)
button.add_shape(button_body)
button_hitbox = Hitbox([]) # We initialize an empty hitbox.
button_hitbox.add_hitboxobject(HitboxRect(button_hitbox, Coord(0,0), Coord(2,2), display)) # We add a button hitbox to it.
button.set_hitbox(button_hitbox) # We set the hitbox.
# Now, let's add some text!
button_text = Text(
    origin=Coord(1,1),
    text="Click me to swap my color scheme!"
    )
# We will have to add it to the button.
button.add_shape(button_text)
# Finally, we'll add the button to the display.
display.add_object("button", button)
fps = 60
time.sleep(0.1)

while True:
    if vizwiz.mouse.mouse_down:
        if button.hitbox.on_mouse():
            # We'll swap the color scheme.
            button_body.specs = {
                "fill_color":"purple",
                "color":"pink",
                "width":3
                }
    engine.draw_frame() # Finally, we draw the frame.
    time.sleep(1 / fps)