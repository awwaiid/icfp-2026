from .component import Component

class PipeMerge(Component):
    def init(self, inputs=2):
        # Merge many input streams into one output (top right).
        # Input ports run down the left side, one every 7 rows so they
        # line up with a stack of MemoryCells.
        lines = [
            " +--+",
            ">|>V|>",
            " |@V|",
            " | R|",
            " | S|",
            " |^<|",
        ]
        last_port_row = 1 + 7 * (inputs - 1)
        for y in range(6, last_port_row + 2):
            lines.append(">|  |" if (y - 1) % 7 == 0 else " |  |")
        lines.append(" +--+")
        self.load_from_string("\n".join(lines))
        self.add_port("out", 5, 1)
        for i in range(inputs):
            self.add_port(f"in{i + 1}", 0, 1 + 7 * i)
