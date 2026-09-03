# Vispen Documentation Outline

## 1. Overview
Vispen is a "game" engine for making basic games. It's easy to learn and use.

## 2. Installation
- Requirements
- Installing from wheel
- Installing from GitHub
- Editable install for development

## 3. Quickstart
- Minimal example showing basic usage
- How to create a VizWiz instance
- How to add displays and objects
- How to render

## 4. Core Concepts
- VizWiz
VizWiz is the main container that is for rendering everything.
- Engine
Engine contains the VizWiz and acts like a root.
- Display
Displays are things that the VizWiz contains, and they contain Objects.
- Object
Objects are collections of shapes and/or hitboxes contained by a Display.
- Coord
Coords are coordinates that act like complex numbers. They are relative to whatever they're in, whether it be a shape or an object.
- Utils
utils.py contains some helpful functions that are used by some of the vizwiz.py classes. One important constant is utils.loop, which represents 10<sup>8</sup>. Using a 1:1s conversion rate, it would last ~3.17 years. It can be used in subclasses of Interpolation for looping movement.

## 5. API Reference
### 5.1 vizwiz.py
Classes:
- Coord
- Shape
  - Text
  - Segment
  - Rect
  - Circle
- Hitbox
- HitboxObject
  - HitboxRect
  - HitboxCircle
  - HitboxPoint
- Object
- Interpolation
  - LinTerp
  - SmoothStep
  - SmootherStep
  - TanhTween
- MultInterp
- Looper(MultInterp)
- VizWiz
- Display
- Screen(Display)
- Engine
- Mouse

### 5.2 vizwiz.Coord
Class for coordinates that behave like complex numbers.
Attributes:
- `Coord.x`: The x-coordinate of the object.
- `Coord.y`: The y-coordinate of the object.

Methods:
- `def __init__(self, x: int | float, y: int | float) -> None:` Initialize a coordinate at (x, y).
- `def __add__(self, other: Coord) -> Coord:` Add two coordinates.
- `def __iadd__(self, other: Coord) -> Coord:` Add a coordinate to self in-place.
- `def __sub__(self, other: Coord) -> Coord:` Subtract one coordinate from another.
- `def __mul__(self, other: Coord | int | float) -> Coord:` Multiply two coordinates, or a coordinate by a scalar.
- `def __truediv__(self, other: Coord | int | float) -> Coord:` Divide one coordinate by another or by a scalar.

### 5.3 vizwiz.Shape
`Shape` is a base class that is used in inheritance for the shape subclasses.
Attributes:
- `Shape.origin`: the relative origin of the shape.
- `Shape.specs`: the specifications or characteristics of the shape.

Methods:
- `def __init__(self, origin: Coord, specs: Optional[Dict[str, Any]] = None) -> None:` Initialize the shape.
- `def modify_specs(self, new_specs: Dict[str, Any]) -> None:` Update the shape's drawing specifications.
- `def shift(self, point: Coord) -> None:` Shift the shape by a coordinate acting as a vector.
- `def draw(self, master: Display | Screen, specs: dict | None = None) -> None:` Draw the shape using the given master.

There are currently 4 subclasses:
- `Text`: Text shape.

  Additional attributes:
  - `Text.text`: string to display.

  Modified methods:
  - `def __init__(self, origin: Coord, text: str, specs: Optional[Dict[str, Any]] = None) -> None:` Initialize the text at origin.
- `Segment`: Line segment shape.

  Additional attributes:
  - `Segment.end`: end of the segment.

  Modified methods:
  - `def __init__(self, origin: Coord, end: Coord, specs: Optional[Dict[str, Any]] = None) -> None:` Initialize a segment from origin to end.
- `Rect`: Rectangle shape.

  Additional attributes:
  - `Rect.top_right`: top-right corner of the rectangle.

  Modified methods:
  - `def __init__(self, origin: Coord, top_right: Coord, specs: Optional[Dict[str, Any]] = None) -> None:` Initialize the rectangle from origin to top_right.
- `Circle`: Circle shape.

  Additional attributes:
  - `Circle.radius`: radius of the circle.

  Modified methods:
  - `def __init__(self, origin: Coord, radius: int | float, specs: Optional[Dict[str, Any]] = None) -> None:` Initialize circle at origin with radius.

### 5.4 vizwiz.Hitbox
Class for object hitboxes.
Attributes:
- `Hitbox.shapes`: hitbox objects of the hitbox.

Methods:
- `def __init__(self, shapes: List[HitboxObject]) -> None:` Initializes a hitbox with a list of hitbox objects.
- `def add_hitboxobject(self, shape:HitboxObject) -> None:` Adds a hitbox object to the hitbox.
- `def shift(self, point: Coord) -> None:` Shift all objects in the hitbox.
- `def intersects(self, other: "Hitbox | HitboxObject") -> bool:` Check intersection with another Hitbox or HitboxObject.
- `def on_mouse(self) -> bool:` Check intersection with mouse.

### 5.5 vizwiz.HitboxObject
`HitboxObject` is a base class that is used in inheritance for the shape subclasses.
Attributes:
- `HitboxObject.hitbox`: Hitbox that the hitbox object is in.
- `HitboxObject.origin`: Relative origin of the hitbox object.
- `HitboxObject.master`: Display of the object of the hitbox of the hitbox object.

Methods:
- `def __init__(self, hitbox: Optional[Hitbox], origin: Coord, master: Display) -> None:` Initializes a hitbox object.
- `def convert(self) -> Coord:` Convert local origin to screen coordinates.
- `def shift(self, point: Coord) -> None:` Shift the hitbox object.
- `def intersects(self, other: "HitboxObject | Hitbox") -> bool:` Check intersection with another hitbox object or hitbox.
- `def on_mouse(self) -> bool:` Check intersection with mouse.

There are currently 3 subclasses:
- `HitboxRect`: rectangle hitbox.

  Additional attributes:
  - `HitboxRect.top_right`: top-right corner of the rectangle.

  Modified methods:
  - `def __init__(self, hitbox: Optional[Hitbox], origin: Coord, top_right: Coord, master: Display) -> None:` Initialize a rectangular hitbox object.
- `HitboxCircle`: circle hitbox.

  Additional attributes:
  - `HitboxCircle.radius`: radius of the circle.

  Modified methods:
  - `def __init__(self, hitbox: Optional[Hitbox], origin: Coord, radius: int | float, master: Display) -> None:` Initialize a circular hitbox object.
- `HitboxPoint`: point hitbox.

  Additional attributes: None
  Modified methods: None


### 5.6 vizwiz.Object
- Class descriptions
- Method list

### 5.7 vizwiz.Interpolation
- Class descriptions
- Method list

### 5.8 vizwiz.MultInterp
- Class descriptions
- Method list

### 5.9 vizwiz.VizWiz
- Class descriptions
- Method list

### 5.10 vizwiz.Display
- Class descriptions
- Method list

### 5.11 vizwiz.Engine
- Class descriptions
- Method list

### 5.12 vizwiz.Mouse
- Class descriptions
- Method list

### 5.13 utils.py
- Helper functions

## 6. Examples
- Basic scene
- Multiple objects
- Custom objects
- Coordinate updates
- Rendering variations

## 7. Project Structure
- Folder layout
- Explanation of src/vispen

## 8. Versioning
- Current version
- How versioning works
- How to check vispen.__version__

## 9. Contributing
- How to clone
- How to install in editable mode
- How to submit feedback or PRs

## 10. License
- License type
- Link to LICENSE file
