from .component import Component

class Delay(Component):
    def init(self):
        # Given delay time and pass-through value
        # Count down the delay time and then send the value
        self.load_from_string("""
            +----------+
           >|@>Rb> dRSV|>
            |    ^m<   |
            | ^       <|
            +----------+
        """)
