from gumnut_simulator.GumnutDecoder import GumnutDecoder
from gumnut_simulator import GumnutExceptions


class GumnutCore:
    def __init__(self):
        self.instruction_memory_size = 4096
        self.data_memory_size = 256
        self.IO_controller_register_size = 256
        self.instruction_memory = list()
        self.data_memory = list()
        self.IO_controller_register = list()
        self.PC = 0  # Reset PC to 0
        self.SP = 0  # Reset SP to 0
        self.CARRY = False  # Reset C to False
        self.ZERO = False  # Reset Z to False
        self.WAIT = False  # Reset W to False
        self.STBY = False  # Reset S to False
        self.IREN = False  # Reset I to False
        self.r = [0, 0, 0, 0, 0, 0, 0, 0]
        self.return_address_stack = [0, 0, 0, 0, 0, 0, 0, 0]
        self.IR = False
        self._PC = 0
        self._CARRY = 0
        self._ZERO = 0
        self.reset()
        self.instruction = None
        self.decoder = GumnutDecoder()
        self.data_memory_access_addr = -1
        self.current_ret_line = -1

    def reset(self):
        """Clear all registers, flags, and memory"""
        self.PC = 0  # Reset PC to 0
        self.SP = 0  # Reset SP to 0
        self.CARRY = False  # Reset C to False
        self.ZERO = False  # Reset Z to False
        self.WAIT = False  # Reset W to False
        self.STBY = False  # Reset S to False
        self.IREN = False  # Reset I to False
        self.r = [0, 0, 0, 0, 0, 0, 0, 0]  # Clear registers
        self.return_address_stack = [0, 0, 0, 0, 0, 0, 0, 0]
        self.IR = False
        self._PC = 0
        self._C = 0
        self._Z = 0
        self.data_memory_access_addr = -1
        self.current_ret_line = -1
        self.instruction = None

        # Clear instruction memory
        self.instruction_memory.clear()
        for i in range(0, self.instruction_memory_size, 1):
            self.instruction_memory.insert(i, 0)

        # Clear data memory
        self.data_memory.clear()
        for i in range(0, self.data_memory_size, 1):
            self.data_memory.insert(i, 0)

        # Clear IO controller registers
        self.IO_controller_register.clear()
        for i in range(0, self.IO_controller_register_size, 1):
            self.IO_controller_register.insert(i, 0)

    def upload_instruction_memory(self, data):
        """Upload the instruction memory content as a list to the core"""
        if len(data) > self.instruction_memory_size:
            raise GumnutExceptions.InstructionMemorySizeExceeded(len(data), "Instruction memory size exceeded")
        else:
            self.instruction_memory = data

    def upload_data_memory(self, data):
        """Upload the data memory content as a list to the core"""
        if len(data) > self.data_memory_size:
            raise GumnutExceptions.DataMemorySizeExceeded(len(data), "Data memory size exceeded")
        else:
            self.data_memory = data

    def fetch(self):
        """Fetch the next instruction to execute from program memory"""
        if self.PC >= self.instruction_memory_size:
            raise GumnutExceptions.InvalidPCValue("PC exceeds maximum value", self.PC)
        elif self.PC < 0:
            raise GumnutExceptions.InvalidPCValue("PC exceeds minimum value", self.PC)
        else:
            return self.instruction_memory[self.PC]

    def execute(self, instruction):
        """Execute a single instruction"""
        # Check if we have a valid instruction
        if instruction:
            rd = instruction.rd
            op1 = instruction.op1
            op2 = instruction.op2

            # Arithmetic and logical instructions
            if instruction.instruction == "add":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] + self.r[op2]
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] + op2
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "addc":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] + self.r[op2] + self.CARRY
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] + op2 + self.CARRY
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "sub":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] - self.r[op2]
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] - op2
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "subc":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] - self.r[op2] - self.CARRY
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] - op2 - self.CARRY
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "and":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] & self.r[op2]
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] & op2
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "or":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] | self.r[op2]
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] | op2
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "xor":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] ^ self.r[op2]
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] ^ op2
                self.r[rd] = self.check_range(self.r[rd])

            elif instruction.instruction == "mask":
                if instruction.access == "register":
                    self.r[rd] = self.r[op1] & ~self.r[op2]
                elif instruction.access == "immediate":
                    self.r[rd] = self.r[op1] & ~op2
                self.r[rd] = self.check_range(self.r[rd])

            # Shift instructions
            elif instruction.instruction == "shl":
                self.r[rd] = self.r[op1] << op2
                self.r[rd] &= 0xFF

            elif instruction.instruction == "shr":
                self.r[rd] = self.r[op1] >> op2
                self.r[rd] &= 0xFF

            elif instruction.instruction == "rol":
                _rs = self.r[op1]
                for _ in range(0, op2, 1):
                    carry = (_rs & 0x80) >> 7
                    self.r[rd] = _rs << 1
                    self.r[rd] |= carry
                    self.r[rd] &= 0xFF
                    _rs = self.r[rd]

            elif instruction.instruction == "ror":
                _rs = self.r[op1]
                for _ in range(0, op2, 1):
                    carry = _rs & 0x01
                    self.r[rd] = _rs >> 1
                    self.r[rd] |= carry << 7
                    self.r[rd] &= 0xFF
                    _rs = self.r[rd]

            # Memory and I/O instructions
            elif instruction.instruction == "ldm":
                self.check_data_memory_access(self.r[op1] + op2)
                self.r[rd] = self.data_memory[self.r[op1] + op2]

            elif instruction.instruction == "stm":
                self.check_data_memory_access(self.r[op1] + op2)
                self.data_memory[self.r[op1] + op2] = self.r[rd]

            elif instruction.instruction == "inp":
                self.r[rd] = self.IO_controller_register[self.r[op1] + op2]

            elif instruction.instruction == "out":
                self.IO_controller_register[self.r[op1] + op2] = self.r[rd]

            # Branch instructions
            elif instruction.instruction == "bz":
                if self.ZERO:
                    if op2 & (0x80):
                        self.PC = self.PC + (op2 - 0xFF) - 1
                    else:
                        self.PC = self.PC + op2

            elif instruction.instruction == "bnz":
                if not self.ZERO:
                    if op2 & (0x80):
                        self.PC = self.PC + (op2 - 0xFF) - 1
                    else:
                        self.PC = self.PC + op2

            elif instruction.instruction == "bc":
                if self.CARRY:
                    if op2 & (0x80):
                        self.PC = self.PC + (op2 - 0xFF) - 1
                    else:
                        self.PC = self.PC + op2

            elif instruction.instruction == "bnc":
                if not self.CARRY:
                    if op2 & (0x80):
                        self.PC = self.PC + (op2 - 0xFF) - 1
                    else:
                        self.PC = self.PC + op2

            # Jump instructions
            elif instruction.instruction == "jmp":
                self.PC = op2 - 1

            elif instruction.instruction == "jsb":
                if len(self.return_address_stack) >= 8:
                    self.return_address_stack.pop(0)
                self.return_address_stack.append(self.PC)
                self.SP += 1
                self.PC = op2 - 1

            # Miscellaneous instructions
            elif instruction.instruction == "ret":
                self.SP -= 1
                try:
                    self.PC = self.return_address_stack.pop()
                    if len(self.return_address_stack) < 8:
                        self.return_address_stack.insert(0, 0)
                except IndexError:
                    raise GumnutExceptions.EmptyReturnStack(
                        instruction.instruction, "Attempting to 'ret' while the return-address stack was empty."
                    ) from IndexError

            elif instruction.instruction == "reti":
                self.PC = self._PC - 1
                self.CARRY = self._CARRY
                self.ZERO = self._ZERO
                self.IREN = True
                self.IR = False

            elif instruction.instruction == "enai":
                self.IREN = True

            elif instruction.instruction == "disi":
                self.IREN = False

            elif instruction.instruction == "wait":
                self.WAIT = True

            elif instruction.instruction == "stby":
                self.STBY = True

            # Catch any unknown instructions
            else:
                raise GumnutExceptions.InvalidInstruction(instruction.instruction, "Unknown instruction")
        else:
            raise GumnutExceptions.InvalidInstruction("", "Empty instruction")
        return

    def update_PC(self):
        """Update the PC by adding 1"""
        self.PC += 1
        if self.PC >= self.instruction_memory_size:
            raise GumnutExceptions.InvalidPCValue("PC exceeds maximum value", self.PC)
        elif self.PC < 0:
            raise GumnutExceptions.InvalidPCValue("PC exceeds minimum value", self.PC)
        else:
            return

    def step(self):
        """Perform a single step"""
        if self.IREN and self.IR:
            self.IREN = False
            self.WAIT = False
            self.STBY = False
            self._PC = self.PC
            self._CARRY = self.CARRY
            self._ZERO = self.ZERO
            self.PC = 1
        elif not self.STBY and not self.WAIT:
            objectcode = self.fetch()
            self.instruction = self.decoder.decode_instruction(objectcode)
            self.execute(self.instruction)
            self.r[0] = 0
            self.update_PC()
        return

    def check_range(self, result):
        """Check the result of the current instruction and set flags"""
        if result > 0xFF:
            self.CARRY = True
            return result % 0x100
        elif result < 0:
            self.CARRY = True
            return 0x100 + result
        elif result == 0x00:
            self.ZERO = True
        else:
            self.ZERO = False
            self.CARRY = False

        return result

    def check_data_memory_access(self, address):
        self.data_memory_access_addr = address
        if address > self.data_memory_size:
            raise GumnutExceptions.DataMemoryAccessViolation(address, "Address exceeds maximum value")
