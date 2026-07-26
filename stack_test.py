from src.component import Component
from src.input import Input
from src.output import Output
from src.stack import Stack

class StackTest(Component):
    def init(self):
        inp = Input()
        stack = Stack()
        out = Output()
        self.draw(inp, x=0, y=0)
        self.draw(stack, right_of=inp, spacing=3)
        self.draw(out, right_of=stack, spacing=3)
        self.connect(inp, "out", stack, "in")
        self.connect(stack, "out", out, "in")


if __name__ == "__main__":
    stack_test = StackTest()
    print(stack_test.render())
