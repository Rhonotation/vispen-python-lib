import time
import sys
import os
import keyboard
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from vispen.vizwiz import (
    Engine,
    VizWiz,
    Display,
    Object,
    Coord,
    Rect,
    Hitbox,
    HitboxRect
)

engine = Engine() # First step, creating the engine
vizwiz = VizWiz(width=600, height=400, title="Platformer") # Next, we create the VizWiz
engine.viz = vizwiz
display = Display(
    master=engine.viz,
    origin=Coord(-300, -200),
    top_right=Coord(300, 200),
    id="main",
    scale=50
) # This is how you create the display.
vizwiz.add_display(display)

#Presetting
global level
global levels
global colors
level = 1
levels = {
1: [
    [0,0,0,0,0,0,0,0,0,0,0,4],
    [0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,1,1,0],
    [0,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [5,5,5,5,5,5,5,5,5,5,5,5]
]
}
colors = ['#FFFFFF', '#000000', '#777777', '#2A1503', '#00ED00', '#FF0000', '#FFED00', '#BBBB00']
color_to_number = {color: index for index, color in enumerate(colors)}
#colors 0 'Air    '1 'Ground '2 'One-Way'3 'Sticky '4 'Goal   '5 'Lava   '6 'Jump   '7 'Bounce '.

player = Object(
    master=display,
    origin=Coord(0.1, 2.1),
    id="player",
    shapes=[
        Rect(
            origin=Coord(0, 0),
            top_right=Coord(0.8, 0.8),
            specs={"fill_color": "#6B7AC6", "width": 0}
        )
    ]
)
player_hitbox = Hitbox([])
player_hitbox_rect = HitboxRect(player_hitbox, Coord(0.1, 2.1), Coord(0.9, 2.9), display)
player_hitbox.add_hitboxobject(player_hitbox_rect)
print(player_hitbox.shapes)
player.set_hitbox(player_hitbox)
xvel = 0
yvel = 0
falling = 0
buffer = 0
# This is gonna be a bit weird. We'll need to create a function for creating objects, which are cells, but those objects will also be in an object.

def create_level(level_data):
    global display
    level_object = Object(
        master=display,
        origin=Coord(0, 0),
        id="level"
    )
    for y, row in enumerate(level_data[::-1]):
        for x, cell in enumerate(row):
            if cell != 0:
                cell_object = Object(
                    master=display,
                    origin=Coord(x, y),
                    id=f"cell_{x}_{y}"
                )
                rect = Rect(
                    origin=Coord(0, 0),
                    top_right=Coord(1, 1),
                    specs={"fill_color": colors[cell], "width": 0}
                )
                cell_object.add_shape(rect)
                # now we'll add a hitbox
                hitbox = Hitbox([])
                hitbox_rect = HitboxRect(hitbox, Coord(x, y), Coord(x + 1, y + 1), display)
                hitbox.add_hitboxobject(hitbox_rect)
                cell_object.set_hitbox(hitbox)
                level_object.add_shape(cell_object)
    return level_object

def get_collisions(player: Object, level_object):
    global color_to_number
    collisions = set()
    for shape in level_object.shapes:
        if isinstance(shape, Object) and shape.hitbox and shape.id.startswith("cell_") and isinstance(shape.shapes[0], Rect):
            if player.intersects(shape):
                collisions.add(color_to_number[shape.shapes[0].specs["fill_color"]])
    return collisions

level_object = create_level(levels[level])
level_object.add_shape(player)
display.add_object("level", level_object)

fps = 60
while True:
    print(f"Player position: {player.origin}, Velocity: ({xvel}, {yvel}), Falling: {falling}")
    yvel -= 0.001
    falling += 1
    player.shift(Coord(0, yvel))
    collisions = get_collisions(player, level_object)
    if 1 in collisions or 3 in collisions or (2 in collisions and yvel < 0):
        while 1 in collisions or 2 in collisions or 3 in collisions:
            player.shift(Coord(0, -abs(yvel)/(50 * yvel)))
            collisions = get_collisions(player, level_object)
            if yvel < 0:
                falling = 0
            else:
                falling = 4
        yvel = 0
    if keyboard.is_pressed('up') and falling <= 3:
        yvel = 5
    if keyboard.is_pressed('right'):
        xvel += 0.3
    if keyboard.is_pressed('left'):
        xvel -= 0.3
    xvel *= 0.9
    player.shift(Coord(xvel, 0))
    if 1 in collisions or 3 in collisions:
        if 1 in collisions:
            s = -(5+min(yvel,5))*abs(xvel)/xvel
        if 3 in collisions:
            s = 0
        while 1 in collisions or 3 in collisions:
            player.shift(Coord(-abs(xvel)/(50 * xvel), 0))
            collisions = get_collisions(player, level_object)
        if keyboard.is_pressed('up'):
            yvel = 4
            xvel = s
    engine.draw_frame()
    time.sleep(1 / fps)