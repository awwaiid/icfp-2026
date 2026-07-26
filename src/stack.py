from .component import Component
from .memory import Memory

class Stack(Component):
    def init(self):
        # Store end in b (one past last, starts at 0)
        # Input op; 0=push, 1=pop
        # if push:
        #   1 -> A
        #   Send A to memory (op = write)
        #   Swap A<->B
        #   Send A to memory (slot)
        #   Add A+B -> A (increment top)
        #   Swap A<->B (put top back in B)
        #   Read val -> A
        #   Send A
        #   Loop back to input
        # else:
        #   0 -> A
        #   Send A to memory (op = read)
        #   1 -> A
        #   Swap A<->B
        #   subtract, so A is now old top - 1
        #   Send A to memory (cell with value)
        #   Swap A<->B, so B holds top-1 which is new top
        #   Loop back to input
        #   
        self.load_from_string("""
             +-------------+
            >|@>RX1SWS+WRSV|>
             | ^          <|
             |   >0S1W-SW ^|
             +-------------+
        """)

        # self.load_from_string("""
        #      +----------------+
        #     >|@>RX1SWS+WRS   V|>
        #      | ^             <|
        #      |      >V        |
        #      |   >0-X 0SSW   ^| # What does this do if the stack is empty? Ideally would not break and return 0?
        #      |      >>0S1W-SW^|
        #      +----------------+
        # """)

        memory = Memory()
        self.draw(memory, x=17, y=0)

        self.add_port("in", 0, 1)
        self.add_port("out", *memory.port("out"))
