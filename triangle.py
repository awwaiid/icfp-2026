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

        self.draw_at(0, 0, inp)
        self.draw_at(inp.width, 0, broadcast_pipe)

        self.draw_at(inp.width+broadcast_pipe.width + 5, 0, count_down)

        # Connect broadcast to count_down
        self.draw_pipe([
                inp.width+broadcast_pipe.width - 1, 1,
                inp.width+broadcast_pipe.width + 5, 1
            ])



        self.draw_at(inp.width+broadcast_pipe.width + 5, count_down.height+3, sum_n_nums)

        # Connect broadcast to the sum_n_nums
        self.draw_pipe([
                inp.width+broadcast_pipe.width - 1, 2,
                inp.width+broadcast_pipe.width + 1, 2,
                inp.width+broadcast_pipe.width + 1, count_down.height+4,
                inp.width+broadcast_pipe.width + 5, count_down.height+4
            ])

        # Connect count_down to sum_n_nums (feed the list of numbers to be summed)
        self.draw_pipe([
            inp.width + broadcast_pipe.width + 5 + count_down.width - 1, 1,
            inp.width + broadcast_pipe.width + 5 + count_down.width + 0, 1,
            inp.width + broadcast_pipe.width + 5 + count_down.width + 0, count_down.height + 1,
            inp.width + broadcast_pipe.width + 5 + count_down.width - 7, count_down.height + 1,
            inp.width + broadcast_pipe.width + 5 + count_down.width - 7, count_down.height + 2
        ])




        self.draw_at(inp.width+broadcast_pipe.width + 5 + sum_n_nums.width, count_down.height+3, out)


if __name__ == "__main__":
    triangle = Triangle()
    print(triangle.render())
    # cat.save("cat.man")

