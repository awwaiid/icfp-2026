from textwrap import dedent


def clean(s):
    """Dedent a multi-line string and drop leading/trailing blank lines."""
    lines = dedent(s).split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    return lines


class Canvas:
    """A sparse, auto-expanding 2D grid of characters."""

    def __init__(self):
        self.chars = {}  # (x, y) -> char

    def set(self, x, y, ch):
        self.chars[(x, y)] = ch

    def get(self, x, y):
        return self.chars.get((x, y), " ")

    @property
    def width(self):
        return max(x for x, y in self.chars) + 1 if self.chars else 0

    @property
    def height(self):
        return max(y for x, y in self.chars) + 1 if self.chars else 0

    def place_grid(self, g, x=0, y=0, opaque=False):
        """Place g onto the canvas at (x, y).

        g can be a multi-line string, a list of strings, a Canvas, or a
        Component. Spaces are transparent unless opaque=True.
        """
        if hasattr(g, "canvas"):
            g = g.canvas
        if isinstance(g, Canvas):
            g = str(g).split("\n")
        if isinstance(g, str):
            g = clean(g)
        for dy, line in enumerate(g):
            for dx, ch in enumerate(line):
                if ch != " " or opaque:
                    self.set(x + dx, y + dy, ch)

    def __str__(self):
        return "\n".join(
            "".join(self.get(x, y) for x in range(self.width)).rstrip()
            for y in range(self.height)
        )
