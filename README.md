# Vispen Documentation Outline

## 1. Overview
Vispen is a "game" engine for making basic games. It's easy to learn and use.

## 2. Installation

Vispen is distributed as a standard Python package and can be installed directly from source or in editable mode for development.

### Requirements

- Python 3.10+
- `pip` available in your environment
- (Optional) `pytest` for running tests

### Installing from source

    pip install .

This installs Vispen as a normal package.

### Installing in editable mode (recommended for development)

Editable mode lets you modify the source code and immediately test changes without reinstalling:

    pip install -e .

### Verifying installation

You can confirm Vispen is installed and importable:

    python -c "import vispen; print('Vispen imported successfully')"


## 3. Quickstart
- Minimal example showing basic usage
- How to create a VizWiz instance
- How to add displays and objects
- How to render

## 4. Core Concepts
### VizWiz
VizWiz is the main container that is for rendering everything.
### Engine
Engine contains the VizWiz and acts like a root.
### Display
Displays are things that the VizWiz contains, and they contain Objects.
### Object
Objects are collections of shapes and/or hitboxes contained by a Display.
### Coord
Coords are coordinates that act like complex numbers. They are relative to whatever they're in, whether it be a shape or an object.
### Utils
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
Class for objects.
Attributes:
- `Object.master`: Display of the object.
- `Object.origin`: relative origin of the object.
- `Object.id`: string to identify the object.
- `Object.shapes`: list of shapes of the object.
- `Object.hitbox`: optional hitbox of the object

Methods:
- `def __init__(self, master: "Display | Screen", origin: Coord, id: str, shapes: Optional[List[Shape]] = None, hitbox: Optional[Hitbox] = None) -> None:` Initialize an object.
- `def shift(self, point: Coord) -> None:` Shift the object and its shapes and/or hitbox.
- `def move(self, point: Coord) -> None:` Move the object to a new position.
- `def draw(self) -> None:` Draw all shapes of the object.
- `def intersects(self, other: "Object") -> bool:` Check intersection with another object.
- `def convert(self, point: Coord) -> Coord:` Convert a local point to master's coordinates.
- `def add_shape(self, shape:Shape) -> None:` Add a shape to the object.
- `def add_hitboxobject(self, hitbox:HitboxObject) -> None:` Add a hitbox object to the hitbox.
- `def set_hitbox(self, hitbox:Hitbox) -> None:` Sets the hitbox of the object.

### 5.7 vizwiz.Interpolation
`Interpolation` is a base class for interpolation between two points.
Attributes:
- `Interpolation.start`: start time.
- `Interpolation.duration`: duration.
- `Interpolation.point1`: start point.
- `Interpolation.point2`: end point.

Methods:
- `def __init__(self, start: float, duration: float, point1: Coord, point2: Coord) -> None:` Initializes the interpolation.
- `def finished(self) -> bool:` Return True if the interpolation has finished, and False if it has not.
- `def active(self) -> bool:` Return True if the interpolation is active.
- `def interpolate(self) -> Coord:` Return interpolated coordinate.

There are currently 4 subclasses:
- `LinTerp`: linear interpolation.
- `SmoothStep`: smoothstep interpolation.
- `SmootherStep`: smootherstep interpolation.
- `TanhTween`: tanh-based interpolation. Note that `TanhTween.__init__` takes an extra float argument: sharpness.

### 5.8 vizwiz.MultInterp
Class for multiple interpolations.
Attributes:
- `MultInterp.tweens`: interpolations in order.
- `MultInterp.index`: current interpolation.

Methods:
- `def __init__(self, tweens: Sequence[Interpolation]) -> None:` Initialize the MultInterp.
- `def active(self) -> bool:` Return True if there is an active interpolation.
- `def finished(self) -> bool:` Return True if all interpolations have finished.
- `def interpolate(self) -> Coord:` Return interpolated coordinate from currently active tween.

There is currently one subclass:
- `Looper`: Class for looped interpolations.

  Additional attributes:
  `Looper.start_time`: Start time of the most recent loop.

  Modified methods:
  None

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
Constants:
- `loop`: value equaling 10 ** 8, used in interpolations.

Methods:
- `def distance(point1, point2):` Calculates the Euclidean distance between two Coord objects.
- `def tanhtween(t, sharpness):` Calculates the tween function for the TanhTween.

## 6. Examples
- Basic scene
- Multiple objects
- Custom objects
- Coordinate updates
- Rendering variations

---

## 7. Project Structure

Vispen uses a simple, readable layout that keeps the core library inside `src/vispen` and metadata at the top level.

### Folder layout

```text
    vispen/
    ├── src/
    │   └── vispen/
    │       ├── __init__.py
    │       ├── vizwiz.py
    │       ├── display.py
    │       ├── object.py
    │       ├── coord.py
    │       └── utils.py
    ├── tests/
    ├── pyproject.toml
    ├── README.md
    └── LICENSE
```

### Explanation of `src/vispen`

- `vizwiz.py` — main engine logic (VizWiz, Screen, Engine, Mouse)  
- `display.py` — Display and Screen classes  
- `object.py` — Object definitions and behavior  
- `coord.py` — coordinate math utilities  
- `utils.py` — shared helpers and internal utilities  

---

## 8. Versioning

### Current version

Vispen stores its version in `src/vispen/__init__.py`:

    __version__ = "0.x.y"

### How versioning works

Vispen follows a semantic-style pattern:

- **MAJOR** — breaking API changes  
- **MINOR** — new features, no breaking changes  
- **PATCH** — bug fixes and small improvements  

### How to check `vispen.__version__`

    import vispen
    print(vispen.__version__)

or:

    python -c "import vispen; print(vispen.__version__)"

---

## 9. Contributing

### How to clone

    git clone https://github.com/Rhonotation/vispen-python-lib.git
    cd vispen-python-lib

### How to install in editable mode

    pip install -e .

### How to submit feedback or PRs

1. Open an issue describing the bug or feature request  
2. Fork the repository  
3. Create a branch for your changes  
4. Run tests:

       pytest

5. Open a pull request explaining your changes  

---

## 10. License

### License type

Vispen is released under the **Apache 2.0 License**.

### Link to LICENSE file

    LICENSE

at the root of the repository.