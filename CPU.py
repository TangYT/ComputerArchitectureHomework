class CPU:
	PC = 0          # 程序计数器
	IR = 0          # 指令寄存器
	Register = [0] * 32     # 寄存器
	ALUOuter = 0         # 运算器结果暂存器
	memory = ...

	# cyh添加
	rs1 = 0						# 保存源操作数寄存器1
	rs2 = 0						# 保存源操作数寄存器2
	rd = 0						# 保存目的操作数寄存器
	opcode = 0					# 保存操作码
	imm = 0						# 保存立即数
	width = 0					# 保存读写内存字节数
	func = 0					# 保存指令功能

	rs1_data = 0				# 保存源操作数1
	rs2_data = 0				# 保存源操作数2
	# end

	# 各部件占用情况
	IsBusy = {'PC': False, 'IR': False, 'Register': False, 'ALU': False}
	# 指令类型表，记录指令类型,RISC-V包含4种样式的指令R、I、S、U
	CommandType = {0b000000: 'R', 0b000001: 'I', 0b000010: 'S', 0b0000011: 'U'}
	# 控制信号【还未定义好。。。】
	ControlSignal = []
	# 初始化CPU

	def __init__(self, memory):
		self.PC = 0
		self.IR = 0
		self.Register = [0] * 32
		self.ALUOuter = 0
		self.IsBusy = {'PC': False, 'IR': False, 'Register': False, 'ALU': False}
		self.memory = memory

	# 启动CPU
	def starting_up(self):
		pass

	# 关闭CPU
	def shut_down(self):
		pass

	# 重置CPU
	def reset(self):
		pass

	def setPC(self, mPC):
		self.PC = mPC

	# 占用部件
	def occupy(self, component):
		if self.IsBusy[component]:
			print("CPU运行异常，部件使用发生冲突")
			exit()
			self.IsBusy[component] = True

	# 释放部件
	def release(self, component):
		self.IsBusy[component] = False

	# 取指令,InstructionFetch,从指定
	def IF(self):
		self.occupy('IR')
		self.occupy('PC')

		# 从内存中取出指令，程序寄存器指向下一条指令位置
		self.IR = self.memory.read(self.PC, 4)
		self.PC = self.PC + 4

		self.release('IR')
		self.release('PC')

	# 译码,InstructionDecode
	def ID(self):

		# cyh添加
		self.opcode = 0x0000007f & self.IR
		self.IR = self.IR >> 7
		if self.opcode == 0x00:
			self.rd = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.width = 0x00000007 & self.IR
			self.IR = self.IR >> 3
			self.rs2 = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.imm = 0x00000fff & self.IR
		elif self.opcode == 0x01:
			self.imm = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.width = 0x00000007 & self.IR
			self.IR = self.IR >> 3
			self.rs1 = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.rs2 = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.IR = self.IR << 5
			self.imm = self.imm + self.IR
		elif self.opcode == 0x02:
			self.rd = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.func = 0x00000007 & self.IR
			self.IR = self.IR >> 3
			self.rs1 = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.rs2 = 0x0000001f & self.IR
			self.IR = self.IR >> 5
			self.IR = self.IR << 5
			self.func = self.func + self.IR
	# end

	# 取寄存器,Register Fetch
	def RF(self):
		# cyh添加
		self.occupy('Register')

		self.rs1_data = self.Register[self.rs1]
		self.rs2_data = self.Register[self.rs2]

		self.release('Register')
	# end

	# 执行，Execute
	def EX(self):
		# cyh添加
		self.occupy('ALU')

		if self.opcode == 0x00:
			self.ALUOuter = self.rs2_data+self.imm
		elif self.opcode == 0x01:
			self.ALUOuter = self.rs1_data + self.imm
		elif self.opcode == 0x02:
			self.ALUOuter = self.rs1_data + self.rs2_data

		self.release('ALU')
	# end

	# 访存，Memory
	def MEM(self):

		# cyh添加
		if self.opcode == 0x00:
			self.ALUOuter = self.memory.read(self.ALUOuter, self.width)
		elif self.opcode == 0x01:
			self.memory.write(self.ALUOuter, self.rs2_data, self.width)
	# end

	# 写回，Write Back
	def WB(self):

		# cyh添加
		self.occupy('Register')

		self.Register[self.rd] = self.ALUOuter

		self.release('Register')
	# end

	def run(self):
		for i in range(4):
			self.IF()
			# 如果没有新的指令，结束运行
			if not self.IR:
				break
			self.ID()
			self.RF()
			self.EX()
			self.MEM()
			self.WB()
