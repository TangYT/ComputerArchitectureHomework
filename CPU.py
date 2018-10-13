class CPU:
        PC = 0          # 程序计数器
        IR = 0          # 指令寄存器
        Register = [0] * 32     # 寄存器
        ALUOuter = 0         # 运算器结果暂存器

        # 各部件占用情况
        IsBusy = {'PC': False, 'IR': False, 'Register': False, 'ALU': False}

        # 指令类型表，记录指令类型,RISC-V包含4种样式的指令R、I、S、U
        CommandType = {0b000000: 'R', 0b000001: 'I', 0b000010: 'S', 0b0000011: 'U'}

        # 控制信号【还未定义好。。。】
        ControlSignal = ...

        # 初始化CPU
        def __init__(self):
                self.PC = 0
                self.IR = 0
                self.Register = [0] * 32
                self.ALUOuter = 0
                self.IsBusy = {'PC': False, 'IR': False, 'Register': False, 'ALU': False}

        # 启动CPU
        def starting_up(self):
                ...

        # 关闭CPU
        def shut_down(self):
                ...

        # 重置CPU
        def reset(self):
                ...

        # 占用部件
        def occupy(self, component):
                if self.IsBusy[component]:
                        print("CPU运行异常，部件使用发生冲突")
                        exit()
                self.IsBusy[component] = True

        # 释放部件
        def release(self, component):
                self.IsBusy[component] = False

        # 取指令,InstructionFetch
        def IF(self):
                self.occupy('IR')
                self.occupy('PC')

                # 从内存中取出指令，程序寄存器指向下一条指令位置
                self.IR = ...
                self.PC = self.PC + 4

                self.release('IR')
                self.release('PC')

        # 译码,InstructionDecode
        def ID(self):
                self.occupy('IR')
                self.occupy('PC')

                self.ControlSignal[0] = self.IR / 128
                command_type = self.CommandType[self.ControlSignal[0]]
                if command_type == 'R':
                        self.ControlSignal[1] = ...
                        self.ControlSignal[2] = ...
                        self.ControlSignal[3] = ...
                elif command_type == 'I':
                        self.ControlSignal[1] = ...
                        self.ControlSignal[2] = ...
                        self.ControlSignal[3] = ...
                elif command_type == 'S':
                        self.ControlSignal[1] = ...
                        self.ControlSignal[2] = ...
                        self.ControlSignal[3] = ...
                elif command_type == 'U':
                        self.ControlSignal[1] = ...
                        self.ControlSignal[2] = ...
                        self.ControlSignal[3] = ...

        # 取寄存器,Register Fetch
        def RF(self):
                ...

        # 执行，Execute
        def EX(self):
                if self.ControlSignal[0] == 0:
                        ...
                elif self.ControlSignal[0] == 1:
                        ...

        # 访存，Memory
        def MEM(self):
                ...

        # 写回，Write Back
        def WB(self):
                ...
