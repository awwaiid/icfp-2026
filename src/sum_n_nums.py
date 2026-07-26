from .component import Component

class SumNNums(Component):
    def init(self):
        # Given N, sum N further inputs
        # Algo:
        #   Read N -> A
        #   A -> BP
        #   Done? Yes:
        #     Swap A<->B
        #     Send A
        #     Copy A->B
        #     Subtract A-B which is A-A which is 0->A
        #     Swap A->B, so now B is 0
        #     Loop to start
        #   No:
        #     Read a number -> A
        #     Add A+B -> A
        #     Swap A->B, B is the accumulator
        #     Decrement backpack
        #     loop to done check
        self.load_from_string("""
            +---------+
           >|@>Rb>dWSV|>
            |    mR  M|
            |     +  -|
            |     W  W|
            |    ^<   |
            | ^      <|
            +---------+
        """)
        self.add_port("in", 0, 1)
        # Second input stream (the numbers to sum), fed from above
        self.add_port("in_top", 9, -1, "s")
        self.add_port("out", self.width - 1, 1)
