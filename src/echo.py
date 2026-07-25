
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
