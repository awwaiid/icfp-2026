from .component import Component

class Output(Component):
    def init(self):
        self.load_from_string("""
             +-+
            >|O|
             +-+
        """)
