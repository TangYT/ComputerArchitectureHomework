instruction_set = {'LOAD': 0b0000000, 'STORE': 0b0000001, 'ADD': 0b0000010}
register_set = {'R1': 0b00001, 'R2': 0b00010, 'R3': 0b00011}


def read_instruction():
    s_input = input('~$')
    s_input = s_input.upper()
    if not s_input:
        return 0x00000000
    opr = s_input.split(' ')[0]
    arg = s_input.split(' ')[1].split(',')

    # 如果这是一条LOAD指令(以后重新设计指令集后可统一改为的Ｒ型指令之类的）
    if instruction_set[opr] & 0x000007 == 0:
        instruction = 0x00000000
        instruction = instruction | instruction_set[opr]
        instruction = instruction | (register_set[arg[0]] << 7)
        instruction = instruction | (0b001 << 12)
        instruction = instruction | (0b11111 << 15)
        instruction = instruction | ((0x00000000 + int(arg[1][1:])) << 20)
    # 如果这是一条ＳＴＯＲＥ指令
    elif instruction_set[opr] & 0x000007 == 1:
        instruction = 0x00000000
        instruction = instruction | instruction_set[opr]
        instruction = instruction | ((0x00000000 + int(arg[1][1:]) % 64) << 7)
        instruction = instruction | (0b001 << 12)
        instruction = instruction | (0b11111 << 15)
        instruction = instruction | (register_set[arg[0]] << 20)
        instruction = instruction | ((0x00000000 + int(arg[1][1:]) // 64) << 25)
    elif instruction_set[opr] & 0x000007 == 2:
        instruction = 0x00000000
        instruction = instruction | instruction_set[opr]
        instruction = instruction | (register_set[arg[0]] << 7)
        instruction = instruction | (0b001 << 12)
        instruction = instruction | (register_set[arg[1]] << 15)
        instruction = instruction | (register_set[arg[2]] << 20)
        instruction = instruction | (0x00000000 << 25)
    return instruction
