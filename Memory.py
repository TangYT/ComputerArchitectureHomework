class Memory:
	mem = []

	# 内存初始化
	def Init(self):
		self.mem = [0b00000000]*(1024*1024*4)		# 初始化内存大小为4M(使用32位地址寻址4M)

	# 写函数，使用小端模式存储数据（高位存储在高地址，低位存储在低地址）
	def write(self, addr, data, bytes):		# 内存写操作（地址，数据，字节数（字，半字，字节））
		addr = int(addr)							# 将32位2进制地址转换为10进制
		for i in range(bytes):
			self.mem[addr+i] = 0x000000ff & data		# 按字节存数据的低位
			data = data>>8								# 数据右移八位

	# 读函数
	def read(self, addr, bytes):						# 内存读操作（地址，字节数）
		addr = int(addr)
		data = 0									# 读出的数据
		for i in range(bytes):
			data = data << 8						# 读出数据左移八位
			data = data | self.mem[addr+bytes-i-1]		# 读出剩余数据的高八位
		return data