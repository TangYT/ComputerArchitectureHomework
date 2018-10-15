# -*- coding: utf-8 -*-

from CPU import CPU
from Memory import Memery
from Machine import Machine


cpu = CPU()
memery = Memery()
memery.Init()
machine = Machine()

memery.write(0x00000000,0x010fc080,4)	##向内存写入第一条指令 Load r1,#0(#0的地址为0x00000010)
memery.write(0x00000004,0x014fc100,4)	##向内存写入第二条指令 Load r2,#1(#1的地址为0x00000014)
memery.write(0x00000008,0x00209182,4)	##向内存写入第三条指令 Add r3,r1,r2
memery.write(0x0000000c,0x003fcc01,4)	##向内存写入第四条指令 Store r3,#3(#3的地址为0x00000018)

memery.write(0x00000010,0x11111111,4)
memery.write(0x00000014,0x22222222,4)

machine.starting_up()   ## 开机  # 运行代码

print('0x%8x'%memery.read(0x00000018,4))

machine.shut_down()     ## 关机
