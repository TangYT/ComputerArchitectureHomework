instruction_set = {'LUI':       ['U', 0x00000037],  # 已完成
                   'AUIPC':     ['U', 0x00000017],  # 已完成
                   'JAL':       ['J', 0x0000006F],  # 未使用乱序格式，仅采用顺序编码实现
                   'JALR':      ['I', 0x00000067],  # 已完成
                   'BEQ':       ['B', 0x00000063],  # 未使用乱序格式，仅采用顺序编码实现
                   'BNE':       ['B', 0x00001063],  # 未使用乱序格式，仅采用顺序编码实现
                   'BLT':       ['B', 0x00004063],  # 未使用乱序格式，仅采用顺序编码实现
                   'BGE':       ['B', 0x00005063],  # 未使用乱序格式，仅采用顺序编码实现
                   'BLTU':      ['B', 0x00006063],  # 未使用乱序格式，仅采用顺序编码实现
                   'BGEU':      ['B', 0x00007063],  # 未使用乱序格式，仅采用顺序编码实现
                   'LB':        ['I', 0x00000003],  # 已完成
                   'LH':        ['I', 0x00001003],  # 已完成
                   'LW':        ['I', 0x00002003],  # 已完成
                   'LBU':       ['I', 0x00004003],  # 已完成
                   'LHU':       ['I', 0x00005003],  # 已完成
                   'SB':        ['S', 0x00000023],  # 已完成
                   'SH':        ['S', 0x00001023],  # 已完成
                   'SW':        ['S', 0x00002023],  # 已完成
                   'ADDI':      ['I', 0x00000013],  # 已完成
                   'SLTI':      ['I', 0x00002013],  # 已完成
                   'SLTIU':     ['I', 0x00003013],  # 已完成
                   'XORI':      ['I', 0x00004013],  # 已完成
                   'ORI':       ['I', 0x00006013],  # 已完成
                   'ANDI':      ['I', 0x00007013],  # 已完成
                   'SLLI':      ['I', 0x00001013],  # 已完成
                   'SRLI':      ['I', 0x00005013],  # 已完成
                   'SRAI':      ['I', 0x40005013],  # 已完成
                   'ADD':       ['R', 0x00000033],  # 已完成
                   'SUB':       ['R', 0x40000033],  # 已完成
                   'SLL':       ['R', 0x00001033],  # 已完成
                   'SLT':       ['R', 0x00002033],  # 已完成
                   'SLTU':      ['R', 0x00003033],  # 已完成
                   'XOR':       ['R', 0x00004033],  # 已完成
                   'SRL':       ['R', 0x00005033],  # 已完成
                   'SRA':       ['R', 0x40005033],  # 已完成
                   'OR':        ['R', 0x00006033],  # 已完成
                   'AND':       ['R', 0x00007033],  # 已完成
                   'FENCE':     ['I', 0x0000000F],  # 暂未完成
                   'FENCE.I':   ['I', 0x0000100F],  # 已完成
                   'ECALL':     ['I', 0x00000073],  # 已完成
                   'EBREA':     ['I', 0x00100073],  # 已完成
                   'CSRRW':     ['I', 0x00001073],  # 暂未完成
                   'CSRRS':     ['I', 0x00002073],  # 暂未完成
                   'CSRRC':     ['I', 0x00003073],  # 暂未完成
                   'CSRRWI':    ['I', 0x00005073],  # 暂未完成
                   'CSRRSI':    ['I', 0x00006073],  # 暂未完成
                   'CSRRCI':    ['I', 0x00007073],  # 暂未完成
                   'NOP':       ['I', 0x00000013]}  # 已完成

register_set = {'R0':  0b00000, 'R1':  0b00001, 'R2':  0b00010, 'R3':  0b00011,
                'R4':  0b00100, 'R5':  0b00101, 'R6':  0b00110, 'R7':  0b00111,
                'R8':  0b01000, 'R9':  0b01001, 'R10': 0b01010, 'R11': 0b01011,
                'R12': 0b01100, 'R13': 0b01101, 'R14': 0b01110, 'R15': 0b01111,
                'R16': 0b10000, 'R17': 0b10001, 'R18': 0b10010, 'R19': 0b10011,
                'R20': 0b10100, 'R21': 0b10101, 'R22': 0b10110, 'R23': 0b10111,
                'R24': 0b11000, 'R25': 0b11001, 'R26': 0b11010, 'R27': 0b11011,
                'R28': 0b11100, 'R29': 0b11101, 'R30': 0b11110, 'R31': 0b11111}


def read_instruction():
    s_input = input('~$')
    s_input = s_input.upper()
    if not s_input:
        return 0x00000000
    try:
        opr = s_input.split(' ')[0]
        arg = s_input.split(' ')[1].split(',')

        instruction_type = instruction_set[opr][0]
        instruction = instruction_set[opr][1]
        # 处理一条I型指令
        if instruction_type == 'I':
            if opr in ['CSRRW', 'CSRRS', 'CSRRC', 'CSRRWI', 'CSRRSI', 'CSRRCI', 'FENCE']:
                # 考虑使用概率较低，切尚不清楚状态寄存器结构，故这些指令暂不实现,处理时用空指令替代
                return 0x00000013
            elif opr in ['NOP', 'FENCE.I', 'ECALL', 'EBREA']:
                pass    # 内容已有指令集给定，无参数，不需进行修改
            # 注意到，当偏移量的值准确时，这些指令也可使用I型标准操作去完成
            # elif opr in ['SLLI', 'SRLI', 'SRAI']:
            #     # 移位操作的偏移量只有5位，其余立即数位用来标志移位操作方法为逻辑还是算数
            #     instruction = instruction | (register_set[arg[0]] << 7)
            #     instruction = instruction | (register_set[arg[1]] << 15)
            #     instruction = instruction | ((0b00000 + int(arg[2])) << 20)
            else:
                # 除开上述特殊I型指令，剩余I型指令按标准方法操作
                instruction = instruction | (register_set[arg[0]] << 7)
                instruction = instruction | (register_set[arg[1]] << 15)
                instruction = instruction | ((0b000000000000 + int(arg[2])) << 20)
        # 处理一条R型指令
        elif instruction_type == 'R':
            # R型指令结构统一，均可用相同方式实现
            instruction = instruction | (register_set[arg[0]] << 7)
            instruction = instruction | (register_set[arg[1]] << 15)
            instruction = instruction | (register_set[arg[2]] << 20)
        elif instruction_type in ['S', 'B']:
            # S型指令结构统一，均可用相同方式实现
            instruction = instruction | (register_set[arg[0]] << 20)
            instruction = instruction | (register_set[arg[1]] << 15)
            instruction = instruction | (((0b000000000000 + int(arg[2])) & 0x01F) << 7)
            instruction = instruction | (((0b000000000000 + int(arg[2])) & 0xFE0) << 20)
        elif instruction_type in ['U', 'J']:
            # U型指令结构统一，均可用相同方式实现
            instruction = instruction | (register_set[arg[0]] << 7)
            instruction = instruction | ((0x00000 + int(arg[1])) << 12)
        # 由于虚拟CPU不涉及硬件连线，乱序编码方式过于冗余，在实现时使用顺序编码方式
        # elif instruction_type == 'B':
        #     # B型指令结构统一，均可用相同方式实现
        #     instruction = instruction | (register_set[arg[0]] << 15)
        #     instruction = instruction | (register_set[arg[1]] << 20)
        #     instruction = instruction | (((0b000000000000 + int(arg[2])) & 0x00F) << 8)
        #     instruction = instruction | (((0b000000000000 + int(arg[2])) & 0x400) >> 3)
        #     instruction = instruction | (((0b000000000000 + int(arg[2])) & 0x3F0) << 21)
        #     instruction = instruction | (((0b000000000000 + int(arg[2])) & 0x800) << 20)
        # elif instruction_type == 'J':
        #     pass
        return instruction
    except OSError:
        return 0x00000013

