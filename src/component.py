from .canvas import Canvas, clean


class Component:
    """Base class: owns a canvas and supplies drawing tools.

    Subclasses override init() and draw themselves there.
    """

    def __init__(self, *args, **kwargs):
        self.canvas = Canvas()
        self.init(*args, **kwargs)

    def init(self):
        pass

    def load_from_string(self, s, x=0, y=0):
        """Inject a multi-line string onto the canvas at (x, y)."""
        self.canvas.place_grid(clean(s), x, y)

    def draw_at(self, x, y, thing):
        """Draw a string, Canvas, or Component at (x, y)."""
        self.canvas.place_grid(thing, x, y)

    def draw_pipe(self, points):
        """Draw a pipe through a flat list of coordinates [x1, y1, x2, y2, ...].

        Each consecutive pair of points must form a horizontal or vertical
        segment. Each segment starts with an arrowhead showing its direction
        ('>', '<', 'v', '^'), including a fresh one at every turn, and the
        final endpoint gets one too."""
        if len(points) < 4 or len(points) % 2 != 0:
            raise ValueError("points must be a flat list of at least two x,y pairs")
        pts = [(points[i], points[i + 1]) for i in range(0, len(points), 2)]
        c = self.canvas
        directions = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if y1 == y2:
                step = 1 if x2 > x1 else -1
                for x in range(x1, x2 + step, step):
                    c.set(x, y1, "-")
                directions.append(">" if x2 > x1 else "<")
            elif x1 == x2:
                step = 1 if y2 > y1 else -1
                for y in range(y1, y2 + step, step):
                    c.set(x1, y, "|")
                directions.append("v" if y2 > y1 else "^")
            else:
                raise ValueError(f"segment from {(x1, y1)} to {(x2, y2)} is not horizontal or vertical")
        for (x, y), d in zip(pts, directions):
            c.set(x, y, d)
        c.set(*pts[-1], directions[-1])

    @property
    def width(self):
        return self.canvas.width

    @property
    def height(self):
        return self.canvas.height

    def render(self):
        """Flatten to the output ASCII art string."""
        return str(self.canvas)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.render() + "\n")

    def __str__(self):
        return self.render()
