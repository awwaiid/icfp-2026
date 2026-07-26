import heapq

from .canvas import Canvas, clean

DIRECTIONS = {"e": (1, 0), "w": (-1, 0), "n": (0, -1), "s": (0, 1)}


class Component:
    """Base class: owns a canvas and supplies drawing tools.

    Subclasses override init() and draw themselves there.
    """

    def __init__(self, *args, **kwargs):
        self.canvas = Canvas()
        self.x = 0
        self.y = 0
        self.ports = {}
        self.init(*args, **kwargs)

    def init(self):
        pass

    def load_from_string(self, s, x=0, y=0):
        """Inject a multi-line string onto the canvas at (x, y)."""
        self.canvas.place_grid(clean(s), x, y)

    def draw(self, thing, x=None, y=None, right_of=None, left_of=None,
             below=None, above=None, spacing=0):
        """Draw a string, Canvas, or Component, placed absolutely or
        relative to already-placed components.

        x=/y= give absolute coordinates. right_of=/left_of=other put it
        beside other's edge, top-aligned; below=/above=other put it past
        other's edge, left-aligned. Mix freely — explicit x/y wins over
        the relative anchors. spacing adds that many empty cells of
        separation. Components remember where they were placed, so their
        x/y/right/bottom/ports can position other things afterward.
        (left_of and above need the thing's own size, so they only work
        with Components.)"""
        if x is None:
            if right_of is not None:
                x = right_of.right + spacing
            elif left_of is not None:
                x = left_of.x - spacing - thing.width
            elif below is not None:
                x = below.x
            elif above is not None:
                x = above.x
        if y is None:
            if below is not None:
                y = below.bottom + spacing
            elif above is not None:
                y = above.y - spacing - thing.height
            elif right_of is not None:
                y = right_of.y
            elif left_of is not None:
                y = left_of.y
        if x is None or y is None:
            raise ValueError(
                "draw() couldn't determine a position: give x/y or a relative anchor")
        if isinstance(thing, Component):
            thing.x = x
            thing.y = y
        self.canvas.place_grid(thing, x, y)

    def draw_room_wall(self):
        """Draw a room wall around everything drawn so far: '+' corners,
        '-' along the top/bottom, '|' along the sides, sitting one cell
        outside the current content's bounding box (so leave the top-left
        cell margin free by drawing content starting at (1, 1)).
        Returns the wall bounds (x1, y1, x2, y2)."""
        if not self.canvas.chars:
            raise ValueError("nothing to draw a wall around")
        xs = [x for x, y in self.canvas.chars]
        ys = [y for x, y in self.canvas.chars]
        x1, x2 = min(xs) - 1, max(xs) + 1
        y1, y2 = min(ys) - 1, max(ys) + 1
        for x in range(x1, x2 + 1):
            self.canvas.set(x, y1, "-")
            self.canvas.set(x, y2, "-")
        for y in range(y1, y2 + 1):
            self.canvas.set(x1, y, "|")
            self.canvas.set(x2, y, "|")
        for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
            self.canvas.set(cx, cy, "+")
        return x1, y1, x2, y2

    def add_port(self, name, x, y, direction="e"):
        """Declare a named port at (x, y) relative to this component's
        top-left corner. direction ('e', 'w', 'n', 's') is the way data
        flows through the port."""
        self.ports[name] = (x, y, direction)

    def port(self, name):
        """Absolute (x, y) of a named port, valid once the component is
        placed. Pass the result straight into draw_pipe()."""
        px, py, _ = self.ports[name]
        return (self.x + px, self.y + py)

    def port_direction(self, name):
        return self.ports[name][2]

    def connect(self, src, src_port, dst, dst_port):
        """Auto-route a pipe from src's src_port to dst's dst_port.

        Finds an orthogonal path with as few elbows as possible, leaving
        and entering each port in its flow direction. Anything already
        drawn (components, other pipes) blocks the route, so pipes never
        cross; raises ValueError when no crossing-free route exists."""
        start = src.port(src_port)
        end = dst.port(dst_port)
        sdir = DIRECTIONS[src.port_direction(src_port)]
        edir = DIRECTIONS[dst.port_direction(dst_port)]
        c = self.canvas
        margin = 3
        max_x, max_y = c.width + margin, c.height + margin
        TURN_COST = 10

        def free(x, y):
            return 0 <= x <= max_x and 0 <= y <= max_y and c.get(x, y) == " "

        first = (start[0] + sdir[0], start[1] + sdir[1])
        if first == end:
            if sdir == edir:
                self.draw_pipe([start, end])
                return
            raise ValueError(
                f"ports {src_port} and {dst_port} touch but point different ways")

        # A* over (position, heading); turns cost extra so pipes stay straight
        came_from = {}
        cost = {}
        goal = None
        openq = []
        if free(*first):
            came_from[(first, sdir)] = None
            cost[(first, sdir)] = 0
            openq.append((0, 0, first, sdir))
        counter = 0
        while openq:
            _, _, pos, heading = heapq.heappop(openq)
            if pos == end:
                goal = (pos, heading)
                break
            for d in DIRECTIONS.values():
                if d == (-heading[0], -heading[1]):
                    continue  # a pipe can't double back on itself
                np = (pos[0] + d[0], pos[1] + d[1])
                if np == end:
                    if d != edir:
                        continue  # must enter the destination its way
                elif not free(*np):
                    continue
                ncost = cost[(pos, heading)] + 1 + (TURN_COST if d != heading else 0)
                if ncost < cost.get((np, d), float("inf")):
                    cost[(np, d)] = ncost
                    came_from[(np, d)] = (pos, heading)
                    counter += 1
                    guess = ncost + abs(np[0] - end[0]) + abs(np[1] - end[1])
                    heapq.heappush(openq, (guess, counter, np, d))
        if goal is None:
            raise ValueError(f"no crossing-free route from {start} to {end}")

        # Walk the path back, then keep only the endpoints and elbows
        cells = []
        node = goal
        while node is not None:
            cells.append(node[0])
            node = came_from[node]
        cells.append(start)
        cells.reverse()
        waypoints = [cells[0]]
        for i in range(1, len(cells) - 1):
            before = (cells[i][0] - cells[i - 1][0], cells[i][1] - cells[i - 1][1])
            after = (cells[i + 1][0] - cells[i][0], cells[i + 1][1] - cells[i][1])
            if before != after:
                waypoints.append(cells[i])
        waypoints.append(cells[-1])
        self.draw_pipe(waypoints)

    def draw_pipe(self, points):
        """Draw a pipe through a flat list of coordinates [x1, y1, x2, y2, ...].

        Each consecutive pair of points must form a horizontal or vertical
        segment. Each segment starts with an arrowhead showing its direction
        ('>', '<', 'v', '^'), including a fresh one at every turn, and the
        final endpoint gets one too.

        Entries may also be (x, y) tuples — e.g. from port() — mixed
        freely with bare coordinates."""
        flat = []
        for p in points:
            if isinstance(p, (tuple, list)):
                flat.extend(p)
            else:
                flat.append(p)
        if len(flat) < 4 or len(flat) % 2 != 0:
            raise ValueError("points must flatten to at least two x,y pairs")
        pts = [(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]
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

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    def render(self):
        """Flatten to the output ASCII art string."""
        return str(self.canvas)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.render() + "\n")

    def __str__(self):
        return self.render()
