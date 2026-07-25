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
