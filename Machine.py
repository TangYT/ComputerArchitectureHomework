from Memory import Memory
from CPU import CPU


class Machine:

    def __init__(self):
        self.memory = Memory()
        self.cpu = CPU(self.memory)
        self.memory.Init()

    def starting_up(self):
        self.cpu.run()

    def shut_down(self):
        pass
