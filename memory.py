from src.component import Component
from src.input import Input
from src.output import Output
from src.memory import Memory

class MemoryProblem(Component):
    def init(self):
        inp = Input()
        memory = Memory()
        out = Output()
        self.draw(inp, x=0, y=0)
        self.draw(memory, right_of=inp, spacing=3)
        self.draw(out, right_of=memory, spacing=3)
        self.connect(inp, "out", memory, "in")
        self.connect(memory, "out", out, "in")


if __name__ == "__main__":
    memory_problem = MemoryProblem()
    print(memory_problem.render())
