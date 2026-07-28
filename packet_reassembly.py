from src.component import Component
from src.input import Input
from src.output import Output
from src.memory import Memory
from src.memory_cell import MemoryCell

class Program(Component):
    def init(self):
        # Input: N, (seq, val), (seq, val), ... n-times
        # Output: in seq order from 0 to N
        self.load_from_string("""
              ^                              
             +----------------------------------------------------------------+
            >|                                                                |< # In from memory
             |    V   s                                                  <    |
             |    m                                                           |> # Out to memory
             |   Vd                                                           |
             |V   <                                                           |
             |                                                                |
             | >>>  r                              V    >>    >   >W1sWsV     |  # Read the seq, send op, loc
             | b    V r                                                 <     |  # Read the val
             | r    >                                                 s V     |  # Send the val, now it is stored
             |                                                                |
             |                                                                |
             |        >                                    W0sWsrX V          |  # Read at the given sequence
             |  ^                                                  <          |  # content is zero, so we don't have it, so keep going
             |                                                   >       ^    |  # Content is gt 0
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                                                |
             |                                          W                     |
             |                                          s                     |
             |                                          0                     |
             |                                          W                     |
             |                                          ^<                    |
             |                                     >WrW-X^                    |  # Set as highest if it is higher
             |                                          >W1sWsW0sW^           |  # Send as new highest
             |                                                                |
             |        ^s0                                               <     |
             | ^                                                      <       |
             |>@ 1s0s                                          1s0s0s ^       |  # set highest and get ready to to fetch
             +----------------------------------------------------------------+
                   V  ^                                            V ^
                # seq next to send,                              highest+1 seq received (error when they differ by > 15)
                # actually max+1
        """)
        self.add_port("in", 0, 2)
        self.add_port("out", 2, 0, direction="n")
        self.add_port("memory_in", self.width-1, 2, direction="w")
        self.add_port("memory_out", self.width-1, 4, direction="e")
        self.add_port("next_out", 7, self.height-1, direction="s")
        self.add_port("next_in", 10, self.height-1, direction="n")
        self.add_port("last_out",50, self.height-1, direction="s")
        self.add_port("last_in", 52, self.height-1, direction="n")


class PacketAssembly(Component):
    def init(self):
        inp = Input()
        out = Output()
        prog = Program()
        next_seq = MemoryCell()
        last_seq = MemoryCell()
        store = Memory()

        self.draw(inp, x=0, y=5)
        self.draw(out, x=6, y=0)
        self.draw(prog, below=out, spacing=3)
        self.draw(next_seq, below=prog, spacing=5)
        self.draw(last_seq, below=prog, spacing=5, x=40)
        self.draw(store, right_of=prog, spacing=5)

        self.connect(inp, "out", prog, "in")
        self.connect(prog, "out", out, "in")

        self.connect(prog, "memory_out", store, "in")
        self.connect(store, "out", prog, "memory_in")

        self.connect(prog, "next_out", next_seq, "in")
        self.connect(next_seq, "out", prog, "next_in")

        self.connect(prog, "last_out", last_seq, "in")
        self.connect(last_seq, "out", prog, "last_in")





if __name__ == "__main__":
    packet_assembly = PacketAssembly()
    print(packet_assembly.render())
