class CPU:
	rs1 = 0						# 保存源操作数寄存器1
	rs2 = 0						# 保存源操作数寄存器2
	rd = 0						# 保存目的操作数寄存器
	opcode = 0					# 保存操作码
	opcode_type = None			# 保存操作码类型
	imm = 0						# 保存立即数
	func = 0					# 保存指令功能

	ALUX = 0					# ALU的操作数X
	ALUY = 0					# ALU的操作数Y
	ALUFUNC = 0					# ALU的操作码FUNC
	ALUOuter = 0				# ALU的输出Outer

	CSR = 0x00000000			# 状态寄存器，目前只使用第一位用来标志是否跳转

	# 指令类型表，记录指令类型,RISC-V包含4种样式的指令R、I、S、U
	OpcodeType = {0b0000011: 'LOAD', 0b0000111: 'LOAD_FP', 0b0001011: 'CUSTOM_0', 0b0001111: 'MISC_MEM',
				  0b0010011: 'OP_IMM', 0b0010111: 'AUIPC', 0b0011011: 'OP_IMM_32',
				  0b0100011: 'STORE', 0b0100111: 'STORE_FP', 0b0101011: 'CUSTOM_1', 0b0101111: 'AMO',
				  0b0110011: 'OP', 0b0110111: 'LUI', 0b0111011: 'OP_32',
				  0b1000011: 'MADD', 0b1000111: 'MSUB', 0b1001011: 'NMSUB', 0b1001111: 'NMADD',
				  0b1010011: 'OP-FP', 0b1010111: 'RESERVED', 0b1011011: 'CUSTOM_2/RV128',
				  0b1100011: 'BRANCH', 0b1100111: 'JALR', 0b1101011: 'RESERVED', 0b1101111: 'JAL',
				  0b1110011: 'SYSTEM', 0b1110111: 'RESERVED', 0b1111011: 'CUSTOM_3/RV128',}

	# 初始化CPU
	def __init__(self, memory):
		self.PC = 0
		self.IR = 0
		self.Register = [0x00000000] * 32
		self.ALUOuter = 0
		# 各部件占用情况
		self.IsBusy = {'PC': False, 'IR': False, 'Register': False, 'ALU': False}
		self.memory = memory

	# 启动CPU
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
		self.opcode = self.IR & 0x0000007f
		self.opcode_type = self.OpcodeType[self.opcode]

		# 包含指令LUI,AUIPC,这些指令均采用U格式，
		if self.opcode_type in ['LUI', 'AUIPC']:
			self.rd = (self.IR >> 7) & 0x0001F
			self.imm = ((self.IR >> 12) & 0xFFFFF) << 12
		# 包含指令JAL,这些指令均采用J格式
		if self.opcode_type in ['JAL']:
			self.rd = (self.IR >> 7) & 0x0001F
			self.imm = ((self.IR >> 12) & 0xFFFFF) << 1
		# 包含指令JALR,LB,LH,LW,LBU,LHU,ADDI,SLTI,SLTIU,XORI,ORI,ANDI,SLLI,SRLI,SRAI,NOP,
		# FENCE,FENCE.I,ECALL,EBREA,CSRRW,CSRRS,CSRRC,CSRRWI,CSRRSI,CSRRCI,这些指令均采用I格式
		elif self.opcode_type in ['JALR', 'LOAD', 'OP_IMM', 'MISC_MEM', 'SYSTEM']:
			self.rd = (self.IR >> 7) & 0x0001F
			self.func = (self.IR >> 12) & 0x00007
			self.rs1 = (self.IR >> 15) & 0x0001F
			self.imm = (self.IR >> 20) & 0x00FFF
		# 包含指令ADD,SUB,SLL,SLT,SLTU,XOR,SRL,SRA,OR,AND,这些指令均采用R格式
		elif self.opcode_type in ['OP']:
			self.rd = (self.IR >> 7) & 0x0001F
			self.func = (self.IR >> 12) & 0x00007
			self.rs1 = (self.IR >> 15) & 0x0001F
			self.rs2 = (self.IR >> 20) & 0x0001F
			self.imm = (self.IR >> 25) & 0x0007F		# 就是func7，为节约变量与imm复用
		# 包含指令SB,SH,SW,这些指令均采用S格式
		elif self.opcode_type in ['STORE']:
			self.func = (self.IR >> 12) & 0x00007
			self.rs1 = (self.IR >> 15) & 0x0001F
			self.rs2 = (self.IR >> 20) & 0x0001F
			self.imm = 0x000 | ((self.IR >> 7) & 0x0001F) | (((self.IR >> 25) & 0x07F) << 5)
		# 包含指令BEQ,BNE,BLT,BGE,BLTU,BGEU,这些指令均采用B格式
		elif self.opcode_type in ['BRANCH']:
			self.func = (self.IR >> 12) & 0x00007
			self.rs1 = (self.IR >> 15) & 0x0001F
			self.rs2 = (self.IR >> 20) & 0x0001F
			self.imm = (0x000 | ((self.IR >> 7) & 0x0001F) | (((self.IR >> 25) & 0x07F) << 5)) << 1

	# 取寄存器,Register Fetch
	# 这一阶段的作用是在多发射流水中为不同运算部件准备操作数
	# 暂时还未实现多发射功能，这一阶段用来为ALU指定操作数与操作码
	def RF(self):
		# 包含指令LUI
		if self.opcode_type == 'LUI':
			self.ALUX = self.imm
			self.ALUY = 0
			self.ALUFUNC = 0b0000
		# 包含指令AUIPC,BEQ,BNE,BLT,BGE,BLTU,BGEU,JAL
		elif self.opcode_type in ['AUIPC', 'JAL', 'BRANCH']:
			self.ALUX = self.imm
			self.ALUY = self.PC
			self.ALUFUNC = 0b0000
		# 包含指令JALR,LB,LH,LW,LBU,LHU,SB,SH,SW
		elif self.opcode_type in ['JALR', 'LOAD', 'STORE']:
			self.ALUX = self.Register[self.rs1]
			self.ALUY = self.imm
			self.ALUFUNC = 0b0000
		# 包含指令ADDI,SLTI,SLTIU,XORI,ORI,ANDI,SLLI,SRLI,SRAI,NOP
		elif self.opcode_type == 'OP_IMM':
			self.ALUX = self.Register[self.rs1]
			self.ALUY = self.imm
			self.ALUFUNC = self.func
			if self.ALUFUNC in [0b001, 0b101]:
				self.ALUY = self.ALUY & 0x01F
				self.ALUFUNC = self.ALUFUNC | ((self.ALUY & 0x400) >> 7)
		# 包含指令ADD,SUB,SLL,SLT,SLTU,XOR,SRL,SRA,OR,AND
		elif self.opcode_type == 'OP':
			self.ALUX = self.Register[self.rs1]
			self.ALUY = self.Register[self.rs2]
			self.ALUFUNC = self.func | ((self.imm & 0x20) >> 2)

		# 暂未实现
		# 包含指令FENCE,FENCE.I
		elif self.opcode_type == 'MISC_MEM':
			pass
		# 包含指令ECALL,EBREA,CSRRW,CSRRS,CSRRC,CSRRWI,CSRRSI,CSRRCI
		elif self.opcode_type == 'SYSTEM':
			pass

	# 执行，Execute,根据ALUFUNC对ALU的两个输入进行操作
	def EX(self):
		if self.ALUFUNC == 0b0000:							# ADD
			self.ALUOuter = self.ALUX + self.ALUY
		elif self.ALUFUNC == 0b1000:						# SUB
			self.ALUOuter = self.ALUX - self.ALUY
		elif self.ALUFUNC == 0b0001:						# SLL
			self.ALUOuter = self.ALUX << self.ALUY
		elif self.ALUFUNC == 0b0010:						# SLT
			if int(self.ALUX) < int(self.ALUY):
				self.ALUOuter = 1
			else:
				self.ALUOuter = 0
		elif self.ALUFUNC == 0b0011:						# SLTU
			if self.ALUX < self.ALUY:
				self.ALUOuter = 1
			else:
				self.ALUOuter = 0
		elif self.ALUFUNC == 0b0101:						# SRL
			self.ALUOuter = self.ALUX >> self.ALUY
		elif self.ALUFUNC == 0b1101:						# SRA
			self.ALUOuter = int(self.ALUX) >> self.ALUY
		elif self.ALUFUNC == 0b0100:						# XOR
			self.ALUOuter = self.ALUX ^ self.ALUY
		elif self.ALUFUNC == 0b0110:						# OR
			self.ALUOuter = self.ALUX | self.ALUY
		elif self.ALUFUNC == 0b0111:						# AND
			self.ALUOuter = self.ALUX & self.ALUY

		# 对分支指令进行计算，结果保存到CSR第0位
		if self.opcode_type == 'BRANCH':
			if self.func == 0b000:							# BEQ
				if self.Register[self.rs1] == self.Register[self.rs1]:
					self.CSR = (self.CSR & 0xfffffffe) | 0x00000001
				else:
					self.CSR = self.CSR & 0xfffffffe
			elif self.func == 0b001:						# BNE
				if self.Register[self.rs1] != self.Register[self.rs1]:
					self.CSR = (self.CSR & 0xfffffffe) | 0x00000001
				else:
					self.CSR = self.CSR & 0xfffffffe
			elif self.func == 0b100:						# BLT
				if self.Register[self.rs1] < self.Register[self.rs1]:
					self.CSR = (self.CSR & 0xfffffffe) | 0x00000001
				else:
					self.CSR = self.CSR & 0xfffffffe
			elif self.func == 0b101:						# BGE
				if self.Register[self.rs1] > self.Register[self.rs1]:
					self.CSR = (self.CSR & 0xfffffffe) | 0x00000001
				else:
					self.CSR = self.CSR & 0xfffffffe
			elif self.func == 0b110:						# BLTU
				if int(self.Register[self.rs1]) < int(self.Register[self.rs1]):
					self.CSR = (self.CSR & 0xfffffffe) | 0x00000001
				else:
					self.CSR = self.CSR & 0xfffffffe
			elif self.func == 0b111:						# BGEU
				if int(self.Register[self.rs1]) > int(self.Register[self.rs1]):
					self.CSR = (self.CSR & 0xfffffffe) | 0x00000001
				else:
					self.CSR = self.CSR & 0xfffffffe

	# 访存，Memory，RISC-V中只有LOAD与STORE指令需要访存
	def MEM(self):
		# 包含指令LB,LH,LW,LBU,LHU
		if self.opcode_type == 'LOAD':
			self.ALUOuter = self.memory.read(self.ALUOuter, 2 ** int(self.func & 0b011))
		# 包含指令SB,SH,SW
		elif self.opcode_type == 'STORE':
			self.memory.write(self.ALUOuter, self.Register[self.rs2], 2 ** int(self.func & 0b011))

	# 写回，Write Back,将数据写会寄存器
	def WB(self):
		# 包含指令LUI，AUIPC，ADDI,SLTI,SLTIU,XORI,ORI,ANDI,SLLI,
		# SRLI,SRAI,NOP，ADD,SUB,SLL,SLT,SLTU,XOR,SRL,SRA,OR,AND
		if self.opcode_type in ['LUI', 'AUIPC', 'OP_IMM', 'OP']:
			self.Register[self.rd] = self.ALUOuter
		# 包含指令JAL,JALR
		elif self.opcode_type in ['JAL', 'JALR']:
			self.Register[self.rd] = self.PC
			self.PC = self.ALUOuter
		# 包含指令BEQ,BNE,BLT,BGE,BLTU,BGEU
		elif self.opcode_type == 'BRANCH':
			if self.CSR & 0x00000001:
				self.PC = self.ALUOuter

		# 暂未实现
		# 包含指令FENCE,FENCE.I
		elif self.opcode_type == 'MISC_MEM':
			pass
		# 包含指令ECALL,EBREA,CSRRW,CSRRS,CSRRC,CSRRWI,CSRRSI,CSRRCI
		elif self.opcode_type == 'SYSTEM':
			pass

		# # 包含指令LUI
		# if self.opcode_type == 'LUI':
		# 	pass
		# # 包含指令AUIPC
		# elif self.opcode_type == 'AUIPC':
		# 	pass
		# # 包含指令JAL
		# elif self.opcode_type == 'JAL':
		# 	pass
		# # 包含指令JALR
		# elif self.opcode_type == 'JALR':
		# 	pass
		# # 包含指令BEQ,BNE,BLT,BGE,BLTU,BGEU
		# elif self.opcode_type == 'BRANCH':
		# 	pass
		# # 包含指令LB,LH,LW,LBU,LHU
		# elif self.opcode_type == 'LOAD':
		# 	pass
		# # 包含指令SB,SH,SW
		# elif self.opcode_type == 'STORE':
		# 	pass
		# # 包含指令ADDI,SLTI,SLTIU,XORI,ORI,ANDI,SLLI,SRLI,SRAI,NOP
		# elif self.opcode_type == 'OP_IMM':
		# 	pass
		# # 包含指令ADD,SUB,SLL,SLT,SLTU,XOR,SRL,SRA,OR,AND
		# elif self.opcode_type == 'OP':
		# 	pass
		# # 包含指令FENCE,FENCE.I
		# elif self.opcode_type == 'MISC_MEM':
		# 	pass
		# # 包含指令ECALL,EBREA,CSRRW,CSRRS,CSRRC,CSRRWI,CSRRSI,CSRRCI
		# elif self.opcode_type == 'SYSTEM':
		# 	pass
