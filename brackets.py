from src.component import Component
from src.input import Input
from src.output import Output
from src.stack import Stack
from src.memory_cell import MemoryCell

class Program(Component):
    def init(self):
        # Input: length, v0, v1, v2, ...
        # ascii
        #   ( 40
        #   [ 91
        #   { 123
        #   } 125
        #   ] 93
        #   ) 41
        self.load_from_string("""
                   ^
             +----------------------------------------------------------------------------+
            >|                                                                            |< # Port for stack result
             |                                                                            |
             |                                                                            |> # Port for stack op/val
             |           >WrWV                                                            |  # Consume anything leftover
             |    Vs     dm  <                                                           <|  # Known error
             |                                                                            |  # Send error offset or 0
             |>>rb  d                                                                    ^|  # Input length into BP
             |                                                                            |  # Send error offset or 0
             |      > rV                                                                  |  # Read -> A
             |                   >V        >V         >V                                  |  # Routing
             |         >W `40` - X           >          >  0 s W s                     V  |  # A->B ; If B is 40, 91, or 123 then B<->A, push A; next loop
             |                   >> `91` - X ^                                            |
             |                             >> `123` - X ^                                 |
             |                                                                      >V    |
             |                                                      >        > W1sr-X V   |  #   close match check: A->B, pop->A, if A==B then goto pop is good, else bad
             |                                                >V                    >>  V |  #   else match bad, go send current counter
             |                                        >> `41`-X `40`^ >V                  |  # else if B is 41 then 40->A, goto close match check
             |                                                >> `93`-X `91` ^            |  # else if B is 93 then 91->A, goto close match check
             |                                                        >>`123`^            |  # else 123->A               , goto close match check
             | ^                                                     <                    |  # Post init counter/depth, start looping
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             |                                                                            |
             | >                                                   0srX                  ^|  # Length done, if depth == 0 return 0
             |                        Vrs0                            <                   |  #   else return count
             |                        >                                                  ^|
             |                                                                            |
             | d    ^              >>   +                                                 |  # Not done, keep going
             | m                                                                          |
             |                                                                            |
             | ^                                   V                     sWs1W-W1Wrs0 <   |  # Pop Is good, dec depth, inc count
             | ^              sWs1W+1Wrs0          <                      sWs1W+1Wrs0  <  |  # Push Is good, inc depth, inc count
             |                       Vrs0                                               < |  # Is bad, get count, return it, then reset
             |                       >                                                   ^|  # Send result
             |^                                                      <                    |  # go to read
             |>@  >   1s1s                                      1s0s ^                    |  # Reset counter to 1, depth to 0, go to read
             +----------------------------------------------------------------------------+
                           V  ^                               V    ^                         # Counter, Depth


        """)
        self.add_port("in", 0, 2)
        self.add_port("out", 7, 0, direction="n")
        self.add_port("stack_result_in", self.width-1, 2, direction="w")
        self.add_port("stack_cmd_out", self.width-1, 4, direction="e")
        self.add_port("counter_cmd_out", 15, self.height-1, direction="s")
        self.add_port("counter_in", 18, self.height-1, direction="n")

        self.add_port("depth_cmd_out", 50, self.height-1, direction="s")
        self.add_port("depth_in", 55, self.height-1, direction="n")


class Brackets(Component):
    def init(self):
        inp = Input()
        out = Output()
        prog = Program()
        stack = Stack()
        counter = MemoryCell()
        depth = MemoryCell()
        self.draw(inp, x=0, y=5)
        self.draw(out, x=6, y=0)
        self.draw(prog, below=out, spacing=3)
        self.draw(stack, right_of=prog, spacing=3)
        self.draw(counter, below=prog, spacing=5)
        self.draw(depth, below=prog, spacing=5, x=52)
        # self.draw(out, below=inp, spacing=3)

        self.connect(inp, "out", prog, "in")
        self.connect(prog, "out", out, "in")

        self.connect(prog, "counter_cmd_out", counter, "in")
        self.connect(counter, "out", prog, "counter_in")

        self.connect(prog, "depth_cmd_out", depth, "in")
        self.connect(depth, "out", prog, "depth_in")

        self.connect(prog, "stack_cmd_out", stack, "in")
        self.connect(stack, "out", prog, "stack_result_in")

        # self.connect(inp, "out", stack, "in")
        # self.connect(stack, "out", out, "in")


if __name__ == "__main__":
    brackets = Brackets()
    print(brackets.render())
