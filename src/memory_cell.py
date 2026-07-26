from .component import Component

class MemoryCell(Component):
    def init(self):
        # Input: op, optional value
        # op = 0 -> output stored value
        # op = 1 -> store new value, output nothing
        self.load_from_string("""
             +-------+
            >| V   W<|>
             |@>RXWS^|
             |   R   |
             |   W   |
             | ^ <   |
             +-------+
        """)
        self.add_port("in", 0, 1)
        self.add_port("out", self.width - 1, 1)
