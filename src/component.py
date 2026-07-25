from src.canvas import Canvas, clean


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

    def draw_pipe(self, x1, y1, x2, y2, arrow=True):
        """Draw an L-shaped pipe: horizontal from (x1,y1) to (x2,y1),
        then vertical down/up to (x2,y2). Arrowheads on both ends,
        each pointing along the direction of flow."""
        c = self.canvas
        if x1 != x2:
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                c.set(x, y1, "-")
        if y1 != y2:
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                c.set(x2, y, "|")
            if x1 != x2:
                c.set(x2, y1, "+")
            if arrow:
                c.set(x2, y2, "v" if y2 > y1 else "^")
        elif x1 != x2 and arrow:
            c.set(x2, y1, ">" if x2 > x1 else "<")
        if arrow:
            if x1 != x2:
                c.set(x1, y1, ">" if x2 > x1 else "<")
            elif y1 != y2:
                c.set(x1, y1, "v" if y2 > y1 else "^")

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
