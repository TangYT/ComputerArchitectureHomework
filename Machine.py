from CPU import CPU
from Memory import Memory


class Machine:
    cpu = CPU()       # 实例化一个CPU
    memory = Memory()    # 实例化一个内存

    def __init__(self):
        ...

    def starting_up(self):
        ...

    def shut_down(self):
        ...

    def run(self):
        while True:
            self.cpu.IF()
            self.cpu.ID()
            self.cpu.RF()
            self.cpu.EX()
            self.cpu.MEM()
            self.cpu.WB()
