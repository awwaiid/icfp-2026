from .component import Component

class Input(Component):
    def init(self):
        self.load_from_string("""
            +-+
            |I|>
            +-+
        """)
