# Vispen Documentation Outline

## 1. Overview
- What Vispen is
- What problems it solves
- High‑level description of the engine

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
- Display
- Object
- Coord
- Utils

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
- Coord.x: The x-coordinate of the object.
- Coord.y: The y-coordinate of the object.
Methods:
- def __init__(self, x: int | float, y: int | float) -> None: Initialize a coordinate at (x, y).
- def __add__(self, other: Coord) -> Coord: Add two coordinates.
- def __iadd__(self, other: Coord) -> Coord: Add a coordinate to self in-place.
- def __sub__(self, other: Coord) -> Coord: Subtract one coordinate from another.
- def __mul__(self, other: Coord | int | float) -> Coord: Multiply two coordinates, or a coordinate by a scalar.
- def __truediv__(self, other: Coord | int | float) -> Coord: Divide one coordinate by another or by a scalar.

### 5.3 vizwiz.Shape
Shape is a base class that is used in inheritance for the shape subclasses.
Attributes:
- Shape.origin: the relative origin of the shape.
- Shape.specs: the specifications or characteristics of the shape.
Methods:
- def __init__(self, origin: Coord, specs: Optional[Dict[str, Any]] = None) -> None: Initialize the shape.
- def modify_specs(self, new_specs: Dict[str, Any]) -> None: Update the shape's drawing specifications.
- def shift(self, point: Coord) -> None: Shift the shape by a coordinate acting as a vector.
- def draw(self, master: Display | Screen, specs: dict | None = None) -> None: Draw the shape using the given master.
There are currently 4 subclasses:
- Text: Text shape.
  Additional attributes:
  - Text.text: string to display.

  Modified methods:
  - def __init__(self, origin: Coord, text: str, specs: Optional[Dict[str, Any]] = None) -> None: Initialize the text at origin.
- Segment: Line segment shape.
  Additional attributes:
  - Segment.end: end of the segment.

  Modified methods:
  - def __init__(self, origin: Coord, end: Coord, specs: Optional[Dict[str, Any]] = None) -> None: Initialize a segment from origin to end.
- Rect: Rectangle shape.
  Additional attributes:
  - Rect.top_right: top-right corner of the rectangle.

  Modified methods:
  - def __init__(self, origin: Coord, top_right: Coord, specs: Optional[Dict[str, Any]] = None) -> None: Initialize the rectangle from origin to top_right.
- Circle: Circle shape.
  Additional attributes:
  - Circle.radius: radius of the circle.

  Modified methods:
  - def __init__(self, origin: Coord, radius: int | float, specs: Optional[Dict[str, Any]] = None) -> None: Initialize circle at origin with radius.

### 5.4 vizwiz.Hitbox
- Class descriptions
- Method list

### 5.5 vizwiz.HitboxObject
- Class descriptions
- Method list

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
