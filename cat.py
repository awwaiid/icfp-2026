from src.component import Component
from src.input import Input
from src.output import Output

class Cat(Component):
    def init(self):
        inp = Input()
        out = Output()
        self.draw(inp, x=0, y=0)
        self.draw(out, right_of=inp, spacing=5)
        self.connect(inp, "out", out, "in")


if __name__ == "__main__":
    cat = Cat()
    print(cat.render())
    cat.save("cat.man")
