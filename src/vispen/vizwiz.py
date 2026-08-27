import tkinter
tkinter.NoDefaultRoot()
import turtle
from vispen import utils
import time
import math

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Coord):
            raise ValueError(f"Attempted to add Coord to {type(other).__name__}. Can only add Coord to Coord.")
        return Coord(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        if not isinstance(other, Coord):
            raise ValueError(f"Attempted to add Coord to {type(other).__name__}. Can only add Coord to Coord.")
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Coord(self.x * other, self.y * other)
        elif isinstance(other, Coord):
            return Coord(self.x * other.x - self.y * other.y, self.x * other.y + self.y * other.x) # complex number multiplication
        else:
            raise ValueError(f"Attempted to multiply Coord by {type(other).__name__}. Can only multiply Coord by int, float, or Coord.")

    def __sub__(self, other):
        if not isinstance(other, Coord):
            raise ValueError(f"Attempted to subtract {type(other).__name__} from Coord. Can only subtract Coord from Coord.")
        return Coord(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Coord(self.x / other, self.y / other)
        elif isinstance(other, Coord):
            denom = other.x**2 + other.y**2
            if denom == 0:
                raise ValueError("Attempted to divide by zero Coord.")
            return Coord((self.x * other.x + self.y * other.y) / denom, (self.y * other.x - self.x * other.y) / denom) # complex number division
        else:
            raise ValueError(f"Attempted to divide Coord by {type(other).__name__}. Can only divide Coord by int, float, or Coord.")

class Shape:
    def __init__(self, origin, specs=None):
        self.origin = origin
        self.specs = specs if specs is not None else {}

    def modify_specs(self, new_specs):
        self.specs.update(new_specs)

    def shift(self, point):
        raise NotImplementedError("Subclasses must implement the shift method.")

    def draw(self, master):
        raise NotImplementedError("Subclasses must implement the draw method.")

class Segment(Shape):
    def __init__(self, origin, end, specs=None):
        super().__init__(origin, specs)
        self.end = end

    def shift(self, point):
        self.origin = self.origin + point
        self.end = self.end + point

    def draw(self, master, specs=None):
        master.create_line(self.origin, self.end, specs)

class Rect(Shape):
    def __init__(self, origin, top_right, specs=None):
        super().__init__(origin, specs)
        self.top_right = top_right

    def shift(self, point):
        self.origin = self.origin + point
        self.top_right = self.top_right + point

    def draw(self, master, specs=None):
        master.create_rectangle(self.origin, self.top_right, specs)

class Circle(Shape):
    def __init__(self, origin, radius, specs=None):
        super().__init__(origin, specs)
        self.radius = radius

    def shift(self, point):
        self.origin = self.origin + point

    def draw(self, master, specs=None):
        master.create_circle(self.origin, self.radius, specs)

class Hitbox:
    '''A class representing a hitbox for collision detection. It contains rectangles, circles, and points.'''
    def __init__(self, shapes):
        self.shapes = shapes

    def shift(self, point):
        for shape in self.shapes:
            shape.shift(point)

    def intersects(self, other):
        if isinstance(other, HitboxObject):
            for shape in self.shapes:
                if shape.intersects(other):
                    return True
            return False
        elif isinstance(other, Hitbox):
            for shape1 in self.shapes:
                for shape2 in other.shapes:
                    if shape1.intersects(shape2):
                        return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class HitboxObject:
    '''A class representing a basic hitbox object.'''
    def __init__(self, hitbox, origin, master):
        self.hitbox = hitbox
        self.origin = origin
        self.master = master

    def convert(self):
        return self.master.convert(self.origin)

    def shift(self, point):
        raise NotImplementedError("Subclasses must implement the shift method.")

    def intersects(self, other):
        '''Also, note that this method assumes that both objects are in the same Display or Screen.'''
        raise NotImplementedError("Subclasses must implement the intersects method.")

class HitboxRect(HitboxObject):
    def __init__(self, hitbox, origin, top_right, master):
        super().__init__(hitbox, origin, master)
        self.top_right = top_right

    def shift(self, point):
        self.origin = self.origin + point
        self.top_right = self.top_right + point

    def convert(self):
        return self.master.convert(self.origin), self.master.convert(self.top_right)

    def intersects(self, other):
        if isinstance(other, HitboxRect):
            return not (self.convert()[1].x < other.convert()[0].x or self.convert()[0].x > other.convert()[1].x or
                        self.convert()[1].y < other.convert()[0].y or self.convert()[0].y > other.convert()[1].y)
        elif isinstance(other, HitboxCircle):
            closest_x = max(self.convert()[0].x, min(other.origin.x, self.convert()[1].x))
            closest_y = max(self.convert()[0].y, min(other.origin.y, self.convert()[1].y))
            distance = utils.distance(Coord(closest_x, closest_y), other.origin)
            return distance < other.radius
        elif isinstance(other, HitboxPoint):
            return (other.convert().x >= self.convert()[0].x and other.convert().x <= self.convert()[1].x and
                    other.convert().y >= self.convert()[0].y and other.convert().y <= self.convert()[1].y)
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class HitboxCircle(HitboxObject):
    def __init__(self, hitbox, origin, radius, master):
        super().__init__(hitbox, origin, master)
        self.radius = radius

    def shift(self, point):
        self.origin = self.origin + point

    def convert(self):
        return self.master.convert(self.origin)

    def intersects(self, other):
        if isinstance(other, HitboxCircle):
            distance = utils.distance(self.convert(), other.convert())
            return distance < (self.radius + other.radius)
        elif isinstance(other, HitboxRect):
            closest_x = max(other.convert()[0].x, min(self.convert().x, other.convert()[1].x))
            closest_y = max(other.convert()[0].y, min(self.convert().y, other.convert()[1].y))
            distance = utils.distance(self.convert(), Coord(closest_x, closest_y))
            return distance < self.radius
        elif isinstance(other, HitboxPoint):
            distance = utils.distance(self.convert(), other.convert())
            return distance < self.radius
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class HitboxPoint(HitboxObject):
    def __init__(self, hitbox, origin, master):
        super().__init__(hitbox, origin, master)

    def shift(self, point):
        self.origin = self.origin + point

    def convert(self):
        return self.master.convert(self.origin)

    def intersects(self, other):
        if isinstance(other, HitboxCircle):
            distance = utils.distance(self.convert(), other.convert())
            return distance < other.radius
        elif isinstance(other, HitboxRect):
            return (self.convert().x >= other.convert()[0].x and self.convert().x <= other.convert()[1].x and
                    self.convert().y >= other.convert()[0].y and self.convert().y <= other.convert()[1].y)
        elif isinstance(other, HitboxPoint):
            return self.convert().x == other.convert().x and self.convert().y == other.convert().y
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class Object:
    '''A class containing shapes. Its master is either a Display or Screen.'''
    def __init__(self, master, origin, id, shapes=None, hitbox=None):
        self.master = master
        self.origin = origin
        self.id = id
        if shapes is None:
            shapes = []
        self.shapes = shapes
        if hitbox is None:
            hitbox = Hitbox([])
        self.hitbox = hitbox

    def shift(self, point):
        self.origin = self.origin + point
        if self.hitbox:
            self.hitbox.shift(point)
        if self.shapes:
            for shape in self.shapes:
                shape.shift(point)

    def move(self, point):
        self.shift(point - self.origin)
        self.draw()

    def draw(self):
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.master, shape.specs)

    def intersects(self, other):
        '''Checks intersection.'''
        if self.hitbox and other.hitbox:
            return self.hitbox.intersects(other.hitbox)
        return False

    def convert(self, point):
        '''Converts a point from the object's local coordinates to the master's coordinates.'''
        return point + self.origin

class MultInterp:
    def __init__(self, tweens):
        self.tweens = tweens
        self.index = 0

    def active(self):
        return self.index < len(self.tweens)

    def finished(self):
        return self.index >= len(self.tweens)

    def interpolate(self):
        if not self.active():
            return self.tweens[-1].point2  # Return the last point if all tweens are finished

        current = self.tweens[self.index]
        value = current.interpolate()
        print(f"Current tween index: {self.index}, Value: ({value.x}, {value.y})")  # Debugging line

        # If the current tween finished, move to the next one
        if current.finished():
            self.index += 1

        return value

class Looper(MultInterp):
    def __init__(self, tweens):
        self.tweens = tweens
        self.index = 0
        self.start_time = time.time()

    def interpolate(self):
        if not self.active():
            for tween in self.tweens:
                if isinstance(tween, MultInterp):
                    for stween in tween.tweens:
                        stween.start += time.time() - self.start_time  # Reset start time for each tween
                        tween.index = 0
                else:
                    tween.start += time.time() - self.start_time  # Reset start time for each tween
                    self.start_time = time.time()
            self.index = 0

        current = self.tweens[self.index]
        value = current.interpolate()
        print(f"Current tween index: {self.index}, Value: ({value.x}, {value.y})")  # Debugging line

        # If the current tween finished, move to the next one
        if current.finished():
            self.index += 1

        return value

class Interpolation:
    '''A class for interpolation between two points.'''
    def __init__(self, start, duration, point1, point2):
        self.start = start
        self.duration = duration
        self.point1 = point1
        self.point2 = point2

    def finished(self):
        current_time = time.time()
        return current_time > self.start + self.duration

    def active(self):
        current_time = time.time()
        return (self.start <= current_time) and (current_time <= self.start + self.duration)

    def interpolate(self):
        raise NotImplementedError("Subclasses must implement the interpolate method.")

class LinTerp(Interpolation):
    '''A class for linear interpolation between two points.'''
    def interpolate(self):
        current_time = time.time()
        if current_time < self.start:
            return self.point1
        elif current_time > self.start + self.duration:
            return self.point2
        else:
            t = (current_time - self.start) / self.duration
            x = (1 - t) * self.point1.x + t * self.point2.x
            y = (1 - t) * self.point1.y + t * self.point2.y
            return Coord(x, y)

class SmoothStep(Interpolation):
    '''A class for smooth step interpolation between two points.'''
    def interpolate(self):
        current_time = time.time()
        if current_time < self.start:
            return self.point1
        elif current_time > self.start + self.duration:
            return self.point2
        else:
            t = (current_time - self.start) / self.duration
            t = t * t * (3 - 2 * t)  # Smoothstep function
            x = (1 - t) * self.point1.x + t * self.point2.x
            y = (1 - t) * self.point1.y + t * self.point2.y
            return Coord(x, y)

class SmootherStep(Interpolation):
    '''A class for smoother step interpolation between two points.'''
    def interpolate(self):
        current_time = time.time()
        if current_time < self.start:
            return self.point1
        elif current_time > self.start + self.duration:
            return self.point2
        else:
            t = (current_time - self.start) / self.duration
            t = t * t * t * (t * (6 * t - 15) + 10)  # Smootherstep function
            x = (1 - t) * self.point1.x + t * self.point2.x
            y = (1 - t) * self.point1.y + t * self.point2.y
            return Coord(x, y)

class TanhTween(Interpolation):
    '''A class for smoother step interpolation between two points.'''
    def __init__(self, start, duration, point1, point2, sharpness=3):
        super().__init__(start, duration, point1, point2)
        self.sharpness = sharpness
    
    def interpolate(self):
        current_time = time.time()
        if current_time < self.start:
            return self.point1
        elif current_time > self.start + self.duration:
            return self.point2
        else:
            t = (current_time - self.start) / self.duration
            t = utils.tanhtween(t, self.sharpness)
            x = (1 - t) * self.point1.x + t * self.point2.x
            y = (1 - t) * self.point1.y + t * self.point2.y
            return Coord(x, y)

class VizWiz:
    def __init__(self, width=800, height=600, title="VizWiz Visualization"):
        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.screen.setup(width, height)
        self.screen.title(title)
        self.screen.bgcolor("white")
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.penup()
        self.displays = {}

    def add_display(self, obj):
        if isinstance(obj, Display) or isinstance(obj, Screen):
            self.displays[obj.id] = obj
        self.displays[obj.id] = obj

    def remove_display(self, id):
        if id in self.displays:
            del self.displays[id]

    def draw_frame(self):
        self.turtle.clear()
        for display in self.displays.values():
            display.update_tweens()
            display.draw()
        self.screen.update()

    def create_rectangle(self, origin, top_right, fill=True, color="black", fill_color="black", width=1):
        self.turtle.color(color)
        self.turtle.width(width)
        if fill:
            self.turtle.begin_fill()
            self.turtle.fillcolor(fill_color)
        self.turtle.goto(origin.x, origin.y)
        self.turtle.pendown()
        self.turtle.goto(top_right.x, origin.y)
        self.turtle.goto(top_right.x, top_right.y)
        self.turtle.goto(origin.x, top_right.y)
        self.turtle.goto(origin.x, origin.y)
        self.turtle.penup()
        if fill:
            self.turtle.end_fill()

    def create_circle(self, origin, radius, fill=True, color="black", fill_color="black", width=1):
        self.turtle.color(color)
        self.turtle.width(width)
        if fill:
            self.turtle.begin_fill()
            self.turtle.fillcolor(fill_color)
        self.turtle.goto(origin.x, origin.y - radius)
        self.turtle.pendown()
        self.turtle.circle(radius)
        self.turtle.penup()
        if fill:
            self.turtle.end_fill()

    def create_line(self, origin, end, color="black", width=1):
        self.turtle.color(color)
        self.turtle.width(width)
        self.turtle.goto(origin.x, origin.y)
        self.turtle.pendown()
        self.turtle.goto(end.x, end.y)
        self.turtle.penup()

class Display:
    '''Fixed screen for drawing.'''
    def __init__(self, master, origin, top_right, id, objects = None, scale = 20):
        if objects is None:
            objects = {}
        self.master = master
        self.origin = origin
        self.top_right = top_right
        self.id = id
        self.objects = objects
        self.scale = scale
        self.tweens = {}

    def add_tween(self, id, tween):
        self.tweens[id] = tween

    def remove_tween(self, id):
        if id in self.tweens:
            del self.tweens[id]

    def update_tweens(self):
        for id, tween in self.tweens.items():
            new_position = tween.interpolate()
            self.objects[id].move(new_position)

    def draw(self):
        for obj in self.objects.values():
            obj.draw()

    def create_rectangle(self, origin, top_right, specs=None):
        if specs is None:
            specs = {}
        self.master.create_rectangle(origin * self.scale + self.origin, top_right * self.scale + self.origin, **specs)

    def create_circle(self, origin, radius, specs=None):
        if specs is None:
            specs = {}
        self.master.create_circle(origin * self.scale + self.origin, radius * self.scale, **specs)

    def create_line(self, origin, end, specs=None):
        if specs is None:
            specs = {}
        self.master.create_line(origin * self.scale + self.origin, end * self.scale + self.origin, **specs)

class Screen(Display):
    '''A screen that can be panned and zoomed.'''
    def __init__(self, master, origin, top_right, id, objects = None, scale = 20):
        super().__init__(master, origin, top_right, id, objects, scale)
        self.pan_offset = Coord(0, 0)
        self.zoom_factor = 1.0

    def pan(self, offset):
        self.pan_offset += offset

    def zoom(self, factor):
        self.zoom_factor *= factor

    def convert(self, point):
        return (point * self.scale * self.zoom_factor) + self.origin + self.pan_offset

class Engine:
    def __init__(self):
        self.viz = VizWiz()
        self.displays = {}

    def add_display(self, id, display):
        self.displays[id] = display

    def draw_frame(self):
        self.viz.turtle.clear()
        for display in self.displays.values():
            display.update_tweens()
            display.draw()
        self.viz.screen.update()