from .component import Component

class CountDown(Component):
    def init(self):
        # Given N, output N, N-1, N-2, ..., 1
        self.load_from_string("""
            +------------+
           >|@>Rb>Sm   dV|>
            |    ^ -W1W< |
            | ^         <|
            +------------+
        """)
