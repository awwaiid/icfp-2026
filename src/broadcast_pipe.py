from .component import Component

class BroadcastPipe(Component):
    def init(self):
        # Take one input and send X outputs
        # Hard-wired to 2 for now!
        self.load_from_string("""
            +-----+
           >|@>RSV|>
            | ^  <|>
            +-----+
        """)
        self.add_port("in", 0, 1)
        self.add_port("out1", self.width - 1, 1)
        self.add_port("out2", self.width - 1, 2)
