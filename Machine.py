from Memory import Memory
from CPU import CPU


class Machine:
    memory = Memory()
    cpu = CPU(memory)
    memory.Init()

    def __init__(self):
        pass

    def starting_up(self):
        self.cpu.run()

    def shut_down(self):
        pass
