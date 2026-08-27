import turtle
import utils
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
    def __init__(self, origin):
        self.origin = origin

    def shift(self, point):
        raise NotImplementedError("Subclasses must implement the shift method.")

    def draw(self, master):
        raise NotImplementedError("Subclasses must implement the draw method.")

class Rect(Shape):
    def __init__(self, origin, top_right):
        self.origin = origin
        self.top_right = top_right

    def shift(self, point):
        self.origin = self.origin + point
        self.top_right = self.top_right + point

    def draw(self, master):
        master.create_rectangle(self.origin, self.top_right)

class Circle(Shape):
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

    def shift(self, point):
        self.origin = self.origin + point

    def draw(self, master):
        master.create_circle(self.origin, self.radius)

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
    def __init__(self, hitbox, origin):
        self.hitbox = hitbox
        self.origin = origin

    def shift(self, point):
        raise NotImplementedError("Subclasses must implement the shift method.")

    def intersects(self, other):
        '''Also, note that this method assumes that both objects are in the same Display or Screen.'''
        raise NotImplementedError("Subclasses must implement the intersects method.")

class HitboxRect(HitboxObject):
    def __init__(self, hitbox, origin, top_right):
        super().__init__(hitbox, origin)
        self.top_right = top_right

    def shift(self, point):
        self.origin = self.origin + point
        self.top_right = self.top_right + point

    def intersects(self, other):
        if isinstance(other, HitboxRect):
            return not (self.top_right.x < other.origin.x or self.origin.x > other.top_right.x or
                        self.top_right.y < other.origin.y or self.origin.y > other.top_right.y)
        elif isinstance(other, HitboxCircle):
            closest_x = max(self.origin.x, min(other.origin.x, self.top_right.x))
            closest_y = max(self.origin.y, min(other.origin.y, self.top_right.y))
            distance = utils.distance(Coord(closest_x, closest_y), other.origin)
            return distance < other.radius
        elif isinstance(other, HitboxPoint):
            return (other.origin.x >= self.origin.x and other.origin.x <= self.top_right.x and
                    other.origin.y >= self.origin.y and other.origin.y <= self.top_right.y)
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class HitboxCircle(HitboxObject):
    def __init__(self, hitbox, origin, radius):
        super().__init__(hitbox, origin)
        self.radius = radius

    def shift(self, point):
        self.origin = self.origin + point

    def intersects(self, other):
        if isinstance(other, HitboxCircle):
            distance = utils.distance(self.origin, other.origin)
            return distance < (self.radius + other.radius)
        elif isinstance(other, HitboxRect):
            closest_x = max(other.origin.x, min(self.origin.x, other.top_right.x))
            closest_y = max(other.origin.y, min(self.origin.y, other.top_right.y))
            distance = utils.distance(self.origin, Coord(closest_x, closest_y))
            return distance < self.radius
        elif isinstance(other, HitboxPoint):
            distance = utils.distance(self.origin, other.origin)
            return distance < self.radius
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class HitboxPoint(HitboxObject):
    def __init__(self, hitbox, origin):
        super().__init__(hitbox, origin)

    def shift(self, point):
        self.origin = self.origin + point

    def intersects(self, other):
        if isinstance(other, HitboxCircle):
            distance = utils.distance(self.origin, other.origin)
            return distance < other.radius
        elif isinstance(other, HitboxRect):
            return (self.origin.x >= other.origin.x and self.origin.x <= other.top_right.x and
                    self.origin.y >= other.origin.y and self.origin.y <= other.top_right.y)
        elif isinstance(other, HitboxPoint):
            return self.origin.x == other.origin.x and self.origin.y == other.origin.y
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")

class Object:
    '''A class containing shapes. Its master is either a Display or Screen.'''
    def __init__(self, master, origin, shapes=None, hitbox=None):
        self.master = master
        self.origin = origin
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

    def draw(self):
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.master)

    def intersects(self, other):
        '''Checks intersection.'''
        if self.hitbox and other.hitbox:
            return self.hitbox.intersects(other.hitbox)
        return False

class Interpolation:
    '''A class for interpolation between two points.'''
    def __init__(self, start, duration, point1, point2):
        self.start = start
        self.duration = duration
        self.point1 = point1
        self.point2 = point2

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
        self.screen.setup(width, height)
        self.screen.title(title)
        self.screen.bgcolor("white")
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.penup()

    def create_rectangle(self, origin, top_right, fill=True, color="black", width=1):
        self.turtle.color(color)
        self.turtle.width(width)
        if fill:
            self.turtle.begin_fill()
        self.turtle.goto(origin.x, origin.y)
        self.turtle.pendown()
        self.turtle.goto(top_right.x, origin.y)
        self.turtle.goto(top_right.x, top_right.y)
        self.turtle.goto(origin.x, top_right.y)
        self.turtle.goto(origin.x, origin.y)
        self.turtle.penup()
        if fill:
            self.turtle.end_fill()

    def create_circle(self, origin, radius, fill=True, color="black", width=1):
        self.turtle.color(color)
        self.turtle.width(width)
        if fill:
            self.turtle.begin_fill()
        self.turtle.goto(origin.x, origin.y - radius)
        self.turtle.pendown()
        self.turtle.circle(radius)
        self.turtle.penup()
        if fill:
            self.turtle.end_fill()

class Display:
    '''Fixed screen for drawing.'''
    def __init__(self, master, origin, top_right, shapes = None, scale = 20):
        if shapes is None:
            shapes = []
        self.master = master
        self.origin = origin
        self.top_right = top_right
        self.shapes = shapes
        self.scale = scale

    def create_rectangle(self, origin, top_right):
        self.master.create_rectangle(origin * self.scale + self.origin, top_right * self.scale + self.origin)

    def create_circle(self, origin, radius):
        self.master.create_circle(origin * self.scale + self.origin, radius * self.scale)