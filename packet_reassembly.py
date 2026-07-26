from src.component import Component
from src.input import Input
from src.output import Output
from src.stack import Stack
from src.memory_cell import MemoryCell

class Program(Component):
    def init(self):
        # Input: N, (seq, val), (seq, val), ... n-times
        # Output: in seq order from 0 to N
        self.load_from_string("""
                   ^
             +-----------------------------------------------------------+
            >|                                                           |
             | >r   H                                                    |  # Read the seq
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             |                                                           |
             | ^                                                 <       |
             |>@ 1s0s                                       1s0s ^       |
             +-----------------------------------------------------------+
                   V  ^                                       V ^
                # seq next to send,                         highest+1 seq received (error when they differ by > 15)
                # actually max+1
        """)


class PacketAssembly(Component):
    def init(self):
        prog = Program()
        self.draw(prog, x=0, y=0)


if __name__ == "__main__":
    packet_assembly = PacketAssembly()
    print(packet_assembly.render())
