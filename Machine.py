from Memory import Memory
from CPU import CPU


class Machine:
    cpu = CPU()
    memory = Memory()
    memory.Init()

    def __init__(self):
        self.memery.write(0x00000000, 0x010fc080, 4)  # 向内存写入第一条指令 Load r1,#0(#0的地址为0x00000010)
        self.memery.write(0x00000004, 0x014fc100, 4)  # 向内存写入第二条指令 Load r2,#1(#1的地址为0x00000014)
        self.memery.write(0x00000008, 0x00209182, 4)  # 向内存写入第三条指令 Add r3,r1,r2
        self.memery.write(0x0000000c, 0x003fcc01, 4)  # 向内存写入第四条指令 Store r3,#3(#3的地址为0x00000018)

        self.memery.write(0x00000010, 0x11111111, 4)  # 将0x11111111写入#0
        self.memery.write(0x00000014, 0x22222222, 4)  # 将0x22222222写入#1

    def starting_up(self):
        print('0x%8x' % self.memery.read(0x00000018, 4))
        self.cpu.run()

    def shut_down(self):
        pass

    
