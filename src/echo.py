from .component import Component

class Echo(Component):
    def init(self):
        # Given a number, output it twice
        self.load_from_string("""
            +------+
           >|@>RSSV|>
            | ^   <|
            +------+
        """)
        self.add_port("in", 0, 1)
        self.add_port("out", self.width - 1, 1)
