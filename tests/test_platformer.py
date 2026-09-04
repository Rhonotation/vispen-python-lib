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
    [0,0,0,1,2,1,1,1,5,1,1,1],
    [0,0,0,3,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,1,2,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [1,6,7,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]
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
            specs={"fill_color": "#6B7AC6", "color": "#6B7AC6", "width": 0}
        )
    ]
)
player_hitbox = Hitbox([])
player_hitbox_rect = HitboxRect(player_hitbox, Coord(0.1, 2.1), Coord(0.9, 2.9), display)
player_hitbox.add_hitboxobject(player_hitbox_rect)
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
                if cell == 2:
                    cell_object = Object(
                        master=display,
                        origin=Coord(x, y+0.9),
                        id=f"cell_{x}_{y}"
                    )
                    rect = Rect(
                        origin=Coord(0, 0),
                        top_right=Coord(1, 0.1),
                        specs={"fill_color": colors[cell], "color": colors[cell], "width": 0}
                    )
                else:
                    cell_object = Object(
                        master=display,
                        origin=Coord(x, y),
                        id=f"cell_{x}_{y}"
                    )
                    rect = Rect(
                        origin=Coord(0, 0),
                        top_right=Coord(1, 1),
                        specs={"fill_color": colors[cell], "color": colors[cell], "width": 0}
                    )
                cell_object.add_shape(rect)
                # now we'll add a hitbox
                hitbox = Hitbox([])
                if cell == 2:
                    hitbox_rect = HitboxRect(hitbox, Coord(x, y+0.9), Coord(x + 1, y + 1), display)
                else:
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
while level <= len(levels):
    yvel -= 1/300
    falling += 1
    xvel *= 0.9
    if xvel < 0.01 and xvel > -0.01:
        xvel = 0
    player.shift(Coord(0, yvel))
    collisions = get_collisions(player, level_object)
    if 1 in collisions or 3 in collisions or (2 in collisions and yvel < 0):
        while 1 in collisions or 2 in collisions or 3 in collisions:
            player.shift(Coord(0, -abs(yvel)/(300 * yvel)))
            collisions = get_collisions(player, level_object)
            if yvel < 0:
                falling = 0
            else:
                falling = 5
        yvel = 0
    if keyboard.is_pressed('up') and falling <= 4:
        yvel = 0.07
    if 6 in collisions:
        yvel = 0.13
    if 7 in collisions:
        yvel = 0.17
    if keyboard.is_pressed('right'):
        xvel += 0.02
    if keyboard.is_pressed('left'):
        xvel -= 0.02
    player.shift(Coord(xvel, 0))
    collisions = get_collisions(player, level_object)
    if 1 in collisions or 3 in collisions:
        if 1 in collisions:
            s = -0.25 * abs(xvel)/(xvel)
        if 3 in collisions:
            s = 0
        while 1 in collisions or 3 in collisions:
            player.shift(Coord(-abs(xvel)/(300 * xvel), 0))
            collisions = get_collisions(player, level_object)
        player.shift(Coord(-abs(xvel)/(300 * xvel), 0))
        xvel = 0
        if keyboard.is_pressed('up'):
            yvel = 0.07
            xvel = s
    engine.draw_frame()
    collisions = get_collisions(player, level_object)
    if 4 in collisions:
        level += 1
        if level <= len(levels):
            player.move(Coord(0.1, 2.1))
            display.remove_object("level")
            level_object = create_level(levels[level])
            level_object.add_shape(player)
            display.add_object("level", level_object)
    if 5 in collisions:
        player.move(Coord(0.1, 2.1))
        display.remove_object("level")
        level_object = create_level(levels[level])
        level_object.add_shape(player)
        display.add_object("level", level_object)
    time.sleep(1 / fps)