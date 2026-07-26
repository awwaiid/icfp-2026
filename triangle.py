from src.component import Component
from src.input import Input
from src.output import Output
from src.count_down import CountDown
from src.sum_n_nums import SumNNums
from src.broadcast_pipe import BroadcastPipe

class Triangle(Component):
    def init(self):
        inp = Input()
        out = Output()
        count_down = CountDown()
        sum_n_nums = SumNNums()
        broadcast_pipe = BroadcastPipe()

        self.draw(inp, x=0, y=0)
        self.draw(broadcast_pipe, right_of=inp)
        self.draw(count_down, right_of=broadcast_pipe, spacing=5)
        self.draw(sum_n_nums, below=count_down, spacing=3)
        self.draw(out, right_of=sum_n_nums)

        self.connect(broadcast_pipe, "out1", count_down, "in")
        self.connect(broadcast_pipe, "out2", sum_n_nums, "in")
        # Feed the list of numbers to be summed
        self.connect(count_down, "out", sum_n_nums, "in_top")


if __name__ == "__main__":
    triangle = Triangle()
    print(triangle.render())
    # cat.save("cat.man")

