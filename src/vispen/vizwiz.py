"""
Vispen v1.1.2
Features: Mouse functionality
"""
from __future__ import annotations
from typing import Sequence
import time
import tkinter
import turtle
from typing import Any, Dict, List, Optional
from vispen import utils

tkinter.NoDefaultRoot()


class Coord:
    """Class for coordinates that behave like complex numbers."""

    def __init__(self, x: int | float, y: int | float) -> None:
        """Initialize a coordinate at (x, y)."""
        self.x: float = float(x)
        self.y: float = float(y)

    def __add__(self, other: Coord) -> Coord:
        """Add two coordinates."""
        if not isinstance(other, Coord):
            raise ValueError(
                f"Attempted to add Coord to {type(other).__name__}. "
                "Can only add Coord to Coord."
            )
        return Coord(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Coord) -> Coord:
        """Add a coordinate to self in-place."""
        if not isinstance(other, Coord):
            raise ValueError(
                f"Attempted to add Coord to {type(other).__name__}. "
                "Can only add Coord to Coord."
            )
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other: Coord | int | float) -> Coord:
        """Multiply two coordinates, or a coordinate by a scalar."""
        if isinstance(other, (int, float)):
            return Coord(self.x * other, self.y * other)
        elif isinstance(other, Coord):
            return Coord(
                self.x * other.x - self.y * other.y,
                self.x * other.y + self.y * other.x,
            )
        else:
            raise ValueError(
                f"Attempted to multiply Coord by {type(other).__name__}. "
                "Can only multiply Coord by int, float, or Coord."
            )

    def __sub__(self, other: Coord) -> Coord:
        """Subtract one coordinate from another."""
        if not isinstance(other, Coord):
            raise ValueError(
                f"Attempted to subtract {type(other).__name__} from Coord. "
                "Can only subtract Coord from Coord."
            )
        return Coord(self.x - other.x, self.y - other.y)

    def __truediv__(self, other: Coord | int | float) -> Coord:
        """Divide one coordinate by another or by a scalar."""
        if isinstance(other, (int, float)):
            return Coord(self.x / other, self.y / other)
        elif isinstance(other, Coord):
            denom = other.x**2 + other.y**2
            if denom == 0:
                raise ValueError("Attempted to divide by zero Coord.")
            return Coord(
                (self.x * other.x + self.y * other.y) / denom,
                (self.y * other.x - self.x * other.y) / denom,
            )
        else:
            raise ValueError(
                f"Attempted to divide Coord by {type(other).__name__}. "
                "Can only divide Coord by int, float, or Coord."
            )


class Shape:
    """Base class for drawable shapes."""

    def __init__(self, origin: Coord, specs: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the shape.

        origin: relative origin of the shape.
        specs: drawing specifications (color, fill_color, width, etc.).
        """
        self.origin: Coord = origin
        self.specs: Dict[str, Any] = specs if specs is not None else {}

    def modify_specs(self, new_specs: Dict[str, Any]) -> None:
        """Update the shape's drawing specifications."""
        self.specs.update(new_specs)

    def shift(self, point: Coord) -> None:
        """Shift the shape by a coordinate acting as a vector."""
        raise NotImplementedError("Subclasses must implement the shift method.")

    def draw(self, master: Display | Screen, specs: dict | None = None) -> None:
        """Draw the shape using the given master."""
        raise NotImplementedError("Subclasses must implement the draw method.")


class Text(Shape):
    """Text shape."""

    def __init__(self, origin: Coord, text: str, specs: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize text.

        origin: relative origin.
        text: string to display.
        specs: drawing specifications.
        """
        super().__init__(origin, specs)
        self.text: str = text

    def shift(self, point: Coord) -> None:
        """Shift the text by a coordinate acting as a vector."""
        self.origin = self.origin + point

    def draw(self, master: "Display | Screen", specs: Optional[Dict[str, Any]] = None) -> None:
        """Draw the text using the given master."""
        if specs is None:
            specs = self.specs
        master.create_text(self.origin, self.text, specs)


class Segment(Shape):
    """Line segment shape."""

    def __init__(self, origin: Coord, end: Coord, specs: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a segment from origin to end."""
        super().__init__(origin, specs)
        self.end: Coord = end

    def shift(self, point: Coord) -> None:
        """Shift the segment by a coordinate acting as a vector."""
        self.origin = self.origin + point
        self.end = self.end + point

    def draw(self, master: "Display | Screen", specs: Optional[Dict[str, Any]] = None) -> None:
        """Draw the segment using the given master."""
        if specs is None:
            specs = self.specs
        master.create_line(self.origin, self.end, specs)


class Rect(Shape):
    """Rectangle shape."""

    def __init__(self, origin: Coord, top_right: Coord, specs: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a rectangle from origin to top_right."""
        super().__init__(origin, specs)
        self.top_right: Coord = top_right

    def shift(self, point: Coord) -> None:
        """Shift the rectangle by a coordinate acting as a vector."""
        self.origin = self.origin + point
        self.top_right = self.top_right + point

    def draw(self, master: "Display | Screen", specs: Optional[Dict[str, Any]] = None) -> None:
        """Draw the rectangle using the given master."""
        if specs is None:
            specs = self.specs
        master.create_rectangle(self.origin, self.top_right, specs)


class Circle(Shape):
    """Circle shape."""

    def __init__(self, origin: Coord, radius: int | float, specs: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a circle at origin with given radius."""
        super().__init__(origin, specs)
        self.radius: float = float(radius)

    def shift(self, point: Coord) -> None:
        """Shift the circle by a coordinate acting as a vector."""
        self.origin = self.origin + point

    def draw(self, master: "Display | Screen", specs: Optional[Dict[str, Any]] = None) -> None:
        """Draw the circle using the given master."""
        if specs is None:
            specs = self.specs
        master.create_circle(self.origin, self.radius, specs)


class Hitbox:
    """Hitbox composed of shapes for collision detection."""

    def __init__(self, shapes: List[HitboxObject]) -> None:
        """Initialize a hitbox with a list of hitbox shapes."""
        self.shapes: List[HitboxObject] = shapes

    def add_hitboxobject(self, shape:HitboxObject) -> None:
        """Adds an object to the hitbox."""
        self.shapes.append(shape)

    def shift(self, point: Coord) -> None:
        """Shift all shapes in the hitbox."""
        for shape in self.shapes:
            shape.shift(point)

    def intersects(self, other: "Hitbox | HitboxObject") -> bool:
        """Check intersection with another hitbox or hitbox object."""
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

    def on_mouse(self) -> bool:
        """Check intersection with mouse."""
        for shape in self.shapes:
            if shape.intersects(shape.master.get_mouse_as_hitbox()):
                return True
        return False


class HitboxObject:
    """Base class for hitbox shapes."""

    def __init__(self, hitbox: Optional[Hitbox], origin: Coord, master: Display) -> None:
        """Initialize a hitbox object."""
        self.hitbox: Optional[Hitbox] = hitbox
        self.origin: Coord = origin
        self.master: Display = master

    def convert(self) -> Coord:
        """Convert local origin to screen coordinates."""
        return self.master.convert(self.origin)

    def shift(self, point: Coord) -> None:
        """Shift the hitbox object."""
        raise NotImplementedError("Subclasses must implement the shift method.")

    def intersects(self, other: "HitboxObject | Hitbox") -> bool:
        """Check intersection with another hitbox object or hitbox."""
        raise NotImplementedError("Subclasses must implement the intersects method.")

    def on_mouse(self) -> bool:
        """Check intersection with mouse."""
        return self.intersects(self.master.get_mouse_as_hitbox())


class HitboxRect(HitboxObject):
    """Rectangular hitbox."""

    def __init__(self, hitbox: Optional[Hitbox], origin: Coord, top_right: Coord, master: Display) -> None:
        """Initialize a rectangular hitbox."""
        super().__init__(hitbox, origin, master)
        self.top_right: Coord = top_right

    def shift(self, point: Coord) -> None:
        """Shift the rectangular hitbox."""
        self.origin = self.origin + point
        self.top_right = self.top_right + point

    def convert(self) -> tuple[Coord, Coord]:
        """Convert rectangle corners to screen coordinates."""
        return self.master.convert(self.origin), self.master.convert(self.top_right)

    def intersects(self, other: "HitboxObject | Hitbox") -> bool:
        """Check intersection with another hitbox object or hitbox."""
        if isinstance(other, HitboxRect):
            return not (
                self.convert()[1].x < other.convert()[0].x
                or self.convert()[0].x > other.convert()[1].x
                or self.convert()[1].y < other.convert()[0].y
                or self.convert()[0].y > other.convert()[1].y
            )
        elif isinstance(other, HitboxCircle):
            closest_x = max(self.convert()[0].x, min(other.origin.x, self.convert()[1].x))
            closest_y = max(self.convert()[0].y, min(other.origin.y, self.convert()[1].y))
            distance = utils.distance(Coord(closest_x, closest_y), other.origin)
            return distance < other.radius
        elif isinstance(other, HitboxPoint):
            return (
                other.convert().x >= self.convert()[0].x
                and other.convert().x <= self.convert()[1].x
                and other.convert().y >= self.convert()[0].y
                and other.convert().y <= self.convert()[1].y
            )
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")


class HitboxCircle(HitboxObject):
    """Circular hitbox."""

    def __init__(
        self,
        hitbox: Optional[Hitbox],
        origin: Coord,
        radius: int | float,
        master: Display,
    ) -> None:
        """Initialize a circular hitbox."""
        super().__init__(hitbox, origin, master)
        self.radius: float = float(radius)

    def shift(self, point: Coord) -> None:
        """Shift the circular hitbox."""
        self.origin = self.origin + point

    def convert(self) -> Coord:
        """Convert circle center to screen coordinates."""
        return self.master.convert(self.origin)

    def intersects(self, other: "HitboxObject | Hitbox") -> bool:
        """Check intersection with another hitbox object or hitbox."""
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
    """Point hitbox."""

    def __init__(self, hitbox: Optional[Hitbox], origin: Coord, master: Display) -> None:
        """Initialize a point hitbox."""
        super().__init__(hitbox, origin, master)

    def shift(self, point: Coord) -> None:
        """Shift the point hitbox."""
        self.origin = self.origin + point

    def convert(self) -> Coord:
        """Convert point to screen coordinates."""
        return self.master.convert(self.origin)

    def intersects(self, other: "HitboxObject | Hitbox") -> bool:
        """Check intersection with another hitbox object or hitbox."""
        if isinstance(other, HitboxCircle):
            distance = utils.distance(self.convert(), other.convert())
            return distance < other.radius
        elif isinstance(other, HitboxRect):
            return (
                self.convert().x >= other.convert()[0].x
                and self.convert().x <= other.convert()[1].x
                and self.convert().y >= other.convert()[0].y
                and self.convert().y <= other.convert()[1].y
            )
        elif isinstance(other, HitboxPoint):
            return (
                self.convert().x == other.convert().x
                and self.convert().y == other.convert().y
            )
        elif isinstance(other, Hitbox):
            for shape in other.shapes:
                if self.intersects(shape):
                    return True
            return False
        else:
            raise NotImplementedError("Intersection not implemented for this shape type.")


class Object:
    """Drawable object composed of shapes, with an optional hitbox."""

    def __init__(
        self,
        master: "Display | Screen",
        origin: Coord,
        id: str,
        shapes: Optional[List[Shape]] = None,
        hitbox: Optional[Hitbox] = None,
    ) -> None:
        """Initialize an object with shapes and optional hitbox."""
        self.master: Display | Screen = master
        self.origin: Coord = origin
        self.id: str = id
        self.shapes: List[Shape] = shapes if shapes is not None else []
        self.hitbox: Hitbox = hitbox if hitbox is not None else Hitbox([])

    def shift(self, point: Coord) -> None:
        """Shift the object and its shapes/hitbox."""
        self.origin = self.origin + point
        if self.hitbox:
            self.hitbox.shift(point)
        if self.shapes:
            for shape in self.shapes:
                shape.shift(point)

    def move(self, point: Coord) -> None:
        """Move the object to a new position."""
        self.shift(point - self.origin)
        self.draw()

    def draw(self) -> None:
        """Draw all shapes of the object."""
        if self.shapes:
            for shape in self.shapes:
                shape.draw(self.master, shape.specs)

    def intersects(self, other: "Object") -> bool:
        """Check intersection with another object."""
        if self.hitbox and other.hitbox:
            return self.hitbox.intersects(other.hitbox)
        return False

    def convert(self, point: Coord) -> Coord:
        """Convert a local point to master's coordinates."""
        return point + self.origin

    def add_shape(self, shape:Shape) -> None:
        """Adds a shape to self."""
        self.shapes.append(shape)

    def add_hitboxobject(self, hitbox:HitboxObject) -> None:
        """Adds a hitbox object to the hitbox."""
        self.hitbox.add_hitboxobject(hitbox)

    def set_hitbox(self, hitbox:Hitbox) -> None:
        """Sets the hitbox of self."""
        self.hitbox = hitbox


class Interpolation:
    """Base class for interpolation between two points."""

    def __init__(
        self,
        start: float,
        duration: float,
        point1: Coord,
        point2: Coord,
    ) -> None:
        """Initialize interpolation."""
        self.start: float = start
        self.duration: float = duration
        self.point1: Coord = point1
        self.point2: Coord = point2

    def finished(self) -> bool:
        """Return True if interpolation has finished."""
        current_time = time.time()
        return current_time > self.start + self.duration

    def active(self) -> bool:
        """Return True if interpolation is currently active."""
        current_time = time.time()
        return self.start <= current_time <= self.start + self.duration

    def interpolate(self) -> Coord:
        """Return interpolated coordinate."""
        raise NotImplementedError("Subclasses must implement the interpolate method.")


class LinTerp(Interpolation):
    """Linear interpolation between two points."""

    def interpolate(self) -> Coord:
        """Return linearly interpolated coordinate."""
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
    """Smoothstep interpolation between two points."""

    def interpolate(self) -> Coord:
        """Return smoothstep interpolated coordinate."""
        current_time = time.time()
        if current_time < self.start:
            return self.point1
        elif current_time > self.start + self.duration:
            return self.point2
        else:
            t = (current_time - self.start) / self.duration
            t = t * t * (3 - 2 * t)
            x = (1 - t) * self.point1.x + t * self.point2.x
            y = (1 - t) * self.point1.y + t * self.point2.y
            return Coord(x, y)


class SmootherStep(Interpolation):
    """Smootherstep interpolation between two points."""

    def interpolate(self) -> Coord:
        """Return smootherstep interpolated coordinate."""
        current_time = time.time()
        if current_time < self.start:
            return self.point1
        elif current_time > self.start + self.duration:
            return self.point2
        else:
            t = (current_time - self.start) / self.duration
            t = t * t * t * (t * (6 * t - 15) + 10)
            x = (1 - t) * self.point1.x + t * self.point2.x
            y = (1 - t) * self.point1.y + t * self.point2.y
            return Coord(x, y)


class TanhTween(Interpolation):
    """Tanh-based easing interpolation between two points."""

    def __init__(
        self,
        start: float,
        duration: float,
        point1: Coord,
        point2: Coord,
        sharpness: float = 3.0,
    ) -> None:
        """Initialize tanh tween."""
        super().__init__(start, duration, point1, point2)
        self.sharpness: float = sharpness

    def interpolate(self) -> Coord:
        """Return tanh-eased interpolated coordinate."""
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


class MultInterp:
    """Sequence of interpolations executed in order."""

    def __init__(self, tweens: Sequence[Interpolation]) -> None:
        """Initialize a multi-interpolation chain."""
        self.tweens: Sequence[Interpolation] = tweens
        self.index: int = 0

    def active(self) -> bool:
        """Return True if there are remaining active tweens."""
        return self.index < len(self.tweens)

    def finished(self) -> bool:
        """Return True if all tweens have finished."""
        return self.index >= len(self.tweens)

    def interpolate(self) -> Coord:
        """Return current interpolated coordinate from active tween."""
        if not self.active():
            return self.tweens[-1].point2

        current = self.tweens[self.index]
        value = current.interpolate()

        if current.finished():
            self.index += 1

        return value


class Looper(MultInterp):
    """Looping sequence of interpolations."""

    def __init__(self, tweens: Sequence[Interpolation | MultInterp]) -> None:
        """Initialize a looping interpolation chain."""
        self.tweens: Sequence[Interpolation | MultInterp] = tweens
        self.index: int = 0
        self.start_time: float = time.time()

    def interpolate(self) -> Coord:
        """Return current interpolated coordinate, looping when finished."""
        if not self.active():
            delta = time.time() - self.start_time
            for tween in self.tweens:
                if isinstance(tween, MultInterp):
                    tween.index = 0
                    for stween in tween.tweens:
                        stween.start += delta
                else:
                    tween.start += delta
            self.start_time = time.time()
            self.index = 0

        current = self.tweens[self.index]
        value = current.interpolate()

        if current.finished():
            self.index += 1

        return value


class VizWiz:
    """Visualization wrapper around turtle for drawing displays."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "VizWiz Visualization",
    ) -> None:
        """Initialize VizWiz with a turtle screen."""
        self.screen = turtle.Screen()
        self.screen.tracer(0)
        self.screen.setup(width, height)
        self.screen.title(title)
        self.screen.bgcolor("white")
        self.mouse = Mouse()

        self.turtle: turtle.Turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.penup()

        self.displays: Dict[str, Display | Screen] = {}

        def on_move(event):
            # Convert TK coordinates to turtle coordinates
            x = event.x - self.screen.window_width() / 2
            y = self.screen.window_height() / 2 - event.y
            self.mouse.mouse_pos = [x, y]

        canvas = self.screen.getcanvas()
        canvas.bind("<Motion>", lambda e: on_move(e))
        canvas.bind("<Button-1>", lambda e: self.mouse.on_left_click(e.x, e.y))
        canvas.bind("<Button-2>", lambda e: self.mouse.on_middle_click(e.x, e.y))
        canvas.bind("<Button-3>", lambda e: self.mouse.on_right_click(e.x, e.y))
        canvas.bind("<ButtonRelease-1>", lambda e: self.mouse.on_release(e.x, e.y))
        canvas.bind("<ButtonRelease-2>", lambda e: self.mouse.on_release(e.x, e.y))
        canvas.bind("<ButtonRelease-3>", lambda e: self.mouse.on_release(e.x, e.y))

    def add_display(self, obj: "Display | Screen") -> None:
        """Add a display or screen to the visualization."""
        self.displays[obj.id] = obj

    def remove_display(self, id: str) -> None:
        """Remove a display by id."""
        if id in self.displays:
            del self.displays[id]

    def draw_frame(self) -> None:
        """Draw a single frame for all displays."""
        for display in self.displays.values():
            display.update_tweens()
            display.draw()
        self.screen.update()

    def create_rectangle(
        self,
        origin: Coord,
        top_right: Coord,
        fill: bool = True,
        color: str = "black",
        fill_color: str = "black",
        width: int = 1,
    ) -> None:
        """Draw a rectangle using turtle."""
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

    def create_circle(
        self,
        origin: Coord,
        radius: float,
        fill: bool = True,
        color: str = "black",
        fill_color: str = "black",
        width: int = 1,
    ) -> None:
        """Draw a circle using turtle."""
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

    def create_line(
        self,
        origin: Coord,
        end: Coord,
        color: str = "black",
        width: int = 1,
    ) -> None:
        """Draw a line using turtle."""
        self.turtle.color(color)
        self.turtle.width(width)
        self.turtle.goto(origin.x, origin.y)
        self.turtle.pendown()
        self.turtle.goto(end.x, end.y)
        self.turtle.penup()

    def create_text(
        self,
        origin: Coord,
        text: str,
        color: str = "black",
        font: tuple[str, int, str] = ("Arial", 12, "normal"),
    ) -> None:
        """Draw text using turtle."""
        self.turtle.color(color)
        self.turtle.goto(origin.x, origin.y)
        self.turtle.write(text, font=font)


class Display:
    """Fixed display for drawing objects."""

    def __init__(
        self,
        master: VizWiz,
        origin: Coord,
        top_right: Coord,
        id: str,
        objects: Optional[Dict[str, Object]] = None,
        scale: int = 20,
    ) -> None:
        """Initialize a display."""
        self.master: VizWiz = master
        self.origin: Coord = origin
        self.top_right: Coord = top_right
        self.id: str = id
        self.objects: Dict[str, Object] = objects if objects is not None else {}
        self.scale: int = scale
        self.tweens: Dict[str, MultInterp | Looper | Interpolation] = {}

    def add_tween(self, id: str, tween: MultInterp | Looper | Interpolation) -> None:
        """Add a tween for an object by id."""
        self.tweens[id] = tween

    def remove_tween(self, id: str) -> None:
        """Remove a tween by id."""
        if id in self.tweens:
            del self.tweens[id]

    def update_tweens(self) -> None:
        """Update all tweens and move their objects."""
        for id, tween in self.tweens.items():
            new_position = tween.interpolate()
            self.objects[id].move(new_position)

    def add_object(self, id: str, object: Object) -> None:
        """Add an object by id."""
        self.objects[id] = object

    def remove_object(self, id: str) -> None:
        """Remove an object by id."""
        if id in self.objects:
            del self.objects[id]

    def draw(self) -> None:
        """Draw all objects in the display."""
        for obj in self.objects.values():
            obj.draw()

    def create_rectangle(
        self,
        origin: Coord,
        top_right: Coord,
        specs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a rectangle in display coordinates."""
        if specs is None:
            specs = {}
        self.master.create_rectangle(
            origin * self.scale + self.origin,
            top_right * self.scale + self.origin,
            **specs,
        )

    def create_circle(
        self,
        origin: Coord,
        radius: float,
        specs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a circle in display coordinates."""
        if specs is None:
            specs = {}
        self.master.create_circle(
            origin * self.scale + self.origin,
            radius * self.scale,
            **specs,
        )

    def create_line(
        self,
        origin: Coord,
        end: Coord,
        specs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create a line in display coordinates."""
        if specs is None:
            specs = {}
        self.master.create_line(
            origin * self.scale + self.origin,
            end * self.scale + self.origin,
            **specs,
        )

    def create_text(
        self,
        origin: Coord,
        text: str,
        specs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create text in display coordinates."""
        if specs is None:
            specs = {}
        self.master.create_text(origin * self.scale + self.origin, text, **specs)

    def get_mouse_as_coord(self):
        """Gets the mouse as a coordinate."""
        global mouse_pos
        new_x = (self.master.mouse.mouse_pos[0] - self.origin.x) / self.scale
        new_y = (self.master.mouse.mouse_pos[1] - self.origin.y) / self.scale
        return Coord(new_x, new_y)

    def get_mouse_as_hitbox(self):
        """Gets the mouse as a hitbox."""
        coord = self.get_mouse_as_coord()
        hitbox = Hitbox([])
        hitbox.shapes.append(HitboxPoint(hitbox, coord, self))
        return hitbox

    def convert(self, point:Coord) -> Coord:
        """Convert a local point to screen coordinates."""
        return (point + self.origin) * self.scale


class Screen(Display):
    """Display that supports panning and zooming."""

    def __init__(
        self,
        master: VizWiz,
        origin: Coord,
        top_right: Coord,
        id: str,
        objects: Optional[Dict[str, Object]] = None,
        scale: int = 20,
    ) -> None:
        """Initialize a screen."""
        super().__init__(master, origin, top_right, id, objects, scale)
        self.pan_offset: Coord = Coord(0, 0)
        self.zoom_factor: float = 1.0

    def pan(self, offset: Coord) -> None:
        """Pan the screen by a given offset."""
        self.pan_offset += offset

    def zoom(self, factor: float) -> None:
        """Zoom the screen by a given factor."""
        self.zoom_factor *= factor

    def convert(self, point: Coord) -> Coord:
        """Convert a local point to screen coordinates."""
        return (point * self.scale * self.zoom_factor) + self.origin + self.pan_offset

    def get_mouse_as_coord(self):
        """Gets the mouse as a coordinate."""
        global mouse_pos
        new_x = (self.master.mouse.mouse_pos[0] - self.origin.x - self.pan_offset.x) / self.scale / self.zoom_factor
        new_y = (self.master.mouse.mouse_pos[1] - self.origin.y - self.pan_offset.y) / self.scale / self.zoom_factor
        return Coord(new_x, new_y)


class Engine:
    """Engine that manages VizWiz and displays."""

    def __init__(self) -> None:
        """Initialize the engine."""
        self.viz: VizWiz = VizWiz()
        self.displays: Dict[str, Display | Screen] = {}

    def add_display(self, id: str, display: Display | Screen) -> None:
        """Add a display to the engine."""
        self.displays[id] = display

    def draw_frame(self) -> None:
        """Draw a frame for all displays."""
        self.viz.turtle.clear()
        for display in self.displays.values():
            display.update_tweens()
            display.draw()
        self.viz.screen.update()

class Mouse:
    """Class for a mouse."""
    def __init__(self) -> None:
        """Initializes the mouse."""
        self.mouse_pos: list[float] = [0.0, 0.0]
        self.left_click_down: bool = False
        self.right_click_down: bool = False
        self.middle_click_down: bool = False
        self.mouse_down: bool = False

    def on_left_click(self, x: float, y: float) -> None:
        """Handle left mouse button down."""
        self.left_click_down = True
        self.mouse_down = True

    def on_right_click(self, x: float, y: float) -> None:
        """Handle right mouse button down."""
        self.right_click_down = True
        self.mouse_down = True


    def on_middle_click(self, x: float, y: float) -> None:
        """Handle middle mouse button down."""
        self.middle_click_down = True
        self.mouse_down = True

    def on_release(self, x: float, y: float) -> None:
        """Handle mouse button release."""
        self.left_click_down = False
        self.right_click_down = False
        self.middle_click_down = False
        self.mouse_down = False