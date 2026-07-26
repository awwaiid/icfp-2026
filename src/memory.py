from .component import Component
from .memory_cell import MemoryCell
from .pipe_merge import PipeMerge

class DispatchHeader(Component):
    def init(self):
        # Sets up the get/set
        # Load read/write op (0/1) -> A
        # Load cell num -> BP
        # Load value, if needed -> B
        self.load_from_string("""
            >@RWRbWXV
                   W 
                   R 
                   W 
                   V<
        """)

class DispatchEntry(Component):
    def init(self):
        # Come down to the 'd'
        # If this is not the target, route around dec BP
        # If it is, send the op
        # Then if it is a write, also send the val
        # And then route back up to the top
        self.load_from_string("""
                V  d
                   s
            ^    sWX
            ^      <
                    
                >  V
                   m
        """)

class Dispatcher(Component):
    def init(self):
        header = DispatchHeader()
        entries = [DispatchEntry() for _ in range(0, 100)]

        self.draw(header, x=2, y=1)
        previous = header
        for entry in entries:
            self.draw(entry, below=previous)
            previous = entry

        x1, y1, x2, y2 = self.draw_room_wall()

        # Entry port just left of the wall, feeding the header
        self.canvas.set(x1 - 1, y1 + 1, ">")
        self.add_port("in", x1 - 1, y1 + 1)

        # One east-facing port per entry, just outside the right wall,
        # aligned with the entry's first 's'
        for n, entry in enumerate(entries, start=1):
            port_y = entry.y + 1
            self.canvas.set(x2 + 1, port_y, ">")
            self.add_port(f"cell{n}", x2 + 1, port_y)


class Memory(Component):
    def init(self):
        dispatcher = Dispatcher()
        self.draw(dispatcher, x=0, y=0)

        # A MemoryCell wired to each of the dispatcher's cell ports
        cells = []
        for name in dispatcher.ports:
            if not name.startswith("cell"):
                continue
            px, py = dispatcher.port(name)
            cell = MemoryCell()
            self.draw(cell, x=px + 4, y=py - 1)
            self.connect(dispatcher, name, cell, "in")
            cells.append(cell)

        # Merge all the memory cell outputs into one stream
        merge = PipeMerge(len(cells))
        self.draw(merge, right_of=cells[0], spacing=3)
        for i, cell in enumerate(cells, start=1):
            self.connect(cell, "out", merge, f"in{i}")

        self.add_port("in", *dispatcher.port("in"))
        self.add_port("out", *merge.port("out"))
        



