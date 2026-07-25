from src.component import Component


class Input(Component):
    def init(self):
        self.load_from_string("""
            +-+
            |I|
            +-+
        """)


class Output(Component):
    def init(self):
        self.load_from_string("""
            +-+
            |O|
            +-+
        """)


class Cat(Component):
    def init(self):
        inp = Input()
        out = Output()
        self.draw_at(0, 0, inp)
        self.draw_at(inp.width + 5, 0, out)
        self.draw_pipe(inp.width, 1, inp.width + 4, 1)


if __name__ == "__main__":
    cat = Cat()
    print(cat.render())
    cat.save("cat.man")
