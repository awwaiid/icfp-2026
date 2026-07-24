
from textwrap import dedent

def d(str):
    return dedent(str)[1:-1]

memory_cell = d("""
    +-------+
    | V   W<|
    |@>RXWS^|
    |   R   |
    |   W   |
    | ^ <   |
    +-------+
""")

# So then... imagine ....
# proggie = Proggie()
# proggie.draw_at(x, y, memory_cell)
#
# proggie.print()
#
# also ... these cells should be parameterizable
# Like spin(16)

