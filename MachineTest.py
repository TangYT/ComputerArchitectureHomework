from Machine import Machine
from IOManager import read_instruction

machine = Machine()

# 向内存中写入原始数据
store_place = 0
num_list = input()
num_list = num_list.split(',')
for i in num_list:
    machine.memory.write(store_place, 0x00 + int(i), 1)
    store_place = store_place + 1

# 向内存中写入原始指令
instruction_store_place = store_place
machine.cpu.setPC(instruction_store_place)
instruction = read_instruction()
while instruction:
    machine.memory.write(instruction_store_place, instruction, 4)
    instruction_store_place = instruction_store_place + 4
    instruction = read_instruction()

machine.starting_up()   # 开机，运行代码

# 输出内前4个存储空间，查看结果
print('---------output---------')
for i in range(store_place):
    print('0x%02x' % machine.memory.read(0x00000000 + i, 1))

machine.shut_down()     # 关机
