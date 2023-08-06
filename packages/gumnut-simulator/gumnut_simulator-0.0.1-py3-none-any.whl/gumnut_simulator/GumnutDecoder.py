from collections import namedtuple


INSTR = namedtuple("INSTR", "instruction fn rd op1 op2 access")


def _extract_bitfield(source, width, offset=0):
    """Extract series or a single bit from source"""
    mask = 0
    for _ in range(width):
        mask = (mask << 1) + 1
    result = (source & mask << offset) >> offset
    return result


class GumnutDecoder:
    def __init__(self):
        self.INSTR = INSTR("", "", "", "", "", "")
        self.instruction = INSTR(0, 0, 0, 0, 0, 0)

        self.instruction_masks = [
            0x3F800,  # Misc instructions
            0x3F000,  # Branch instructions
            0x3E000,  # Jump instructions
            # Arithmetic/Logical register access
            0x3C000,
            0x38000,  # Shift instructions
            0x30000,  # Memory and I/O instructions
            0x20000,
        ]  # Arithmetic/Logical immediate access

        self.instructions = [
            0x3F000,  # Misc instructions
            0x3E000,  # Branch instructions
            0x3C000,  # Jump instructions
            0x38000,  # Arithmetic/Logical register access
            0x30000,  # Shift instructions
            0x20000,  # Memory and I/O instructions
            0x00000,
        ]  # Arithmetic/Logical immediate access

    def decode_instruction(self, objectcode):
        """Decode a single instruction and return extracted information"""
        current_instruction = objectcode
        self.instruction = INSTR(0, 0, 0, 0, 0, 0)

        # Loop through all masks
        for i in range(0, 7):
            instruction_mask = self.instruction_masks[i]

            objcode_masked = current_instruction & instruction_mask

            instruction = None
            fn = 0
            rd = 0
            op1 = 0
            op2 = 0
            access = None

            # Check masked objectcode for instruction pattern
            # Arithmetic/Logic REGISTER
            if objcode_masked == self.instructions[3]:
                fn = _extract_bitfield(current_instruction, 3, 0)
                rd = _extract_bitfield(current_instruction, 3, 11)
                op1 = _extract_bitfield(current_instruction, 3, 8)
                op2 = _extract_bitfield(current_instruction, 3, 5)
                access = "register"
                if fn == 0:
                    instruction = "add"
                elif fn == 1:
                    instruction = "addc"
                elif fn == 2:
                    instruction = "sub"
                elif fn == 3:
                    instruction = "subc"
                elif fn == 4:
                    instruction = "and"
                elif fn == 5:
                    instruction = "or"
                elif fn == 6:
                    instruction = "xor"
                elif fn == 7:
                    instruction = "mask"
                break

            # Arithmetic/Logic IMMEDIATE
            if objcode_masked == self.instructions[6]:
                access = "immediate"
                fn = _extract_bitfield(current_instruction, 3, 14)
                rd = _extract_bitfield(current_instruction, 3, 11)
                op1 = _extract_bitfield(current_instruction, 3, 8)
                op2 = _extract_bitfield(current_instruction, 8)
                if fn == 0:
                    instruction = "add"
                elif fn == 1:
                    instruction = "addc"
                elif fn == 2:
                    instruction = "sub"
                elif fn == 3:
                    instruction = "subc"
                elif fn == 4:
                    instruction = "and"
                elif fn == 5:
                    instruction = "or"
                elif fn == 6:
                    instruction = "xor"
                elif fn == 7:
                    instruction = "mask"
                break

            if objcode_masked == self.instructions[4]:
                fn = _extract_bitfield(current_instruction, 3, 0)
                rd = _extract_bitfield(current_instruction, 3, 11)  # rd
                op1 = _extract_bitfield(current_instruction, 3, 8)  # rs
                op2 = _extract_bitfield(current_instruction, 3, 5)  # count
                if fn == 0:
                    instruction = "shl"
                elif fn == 1:
                    instruction = "shr"
                elif fn == 2:
                    instruction = "rol"
                elif fn == 3:
                    instruction = "ror"
                break

            if objcode_masked == self.instructions[5]:
                fn = _extract_bitfield(current_instruction, 3, 14)
                rd = _extract_bitfield(current_instruction, 3, 11)  # rd
                op1 = _extract_bitfield(current_instruction, 3, 8)  # rs
                op2 = _extract_bitfield(current_instruction, 8)  # offset
                if fn == 0:
                    instruction = "ldm"
                elif fn == 1:
                    instruction = "stm"
                elif fn == 2:
                    instruction = "inp"
                elif fn == 3:
                    instruction = "out"
                break

            if objcode_masked == self.instructions[2] and _extract_bitfield(current_instruction, 1, 13) == 0:
                fn = _extract_bitfield(current_instruction, 1, 12)
                rd = 0
                op2 = _extract_bitfield(current_instruction, 12)
                if fn == 0:
                    instruction = "jmp"
                elif fn == 1:
                    instruction = "jsb"
                break

            if objcode_masked == self.instructions[1]:
                fn = _extract_bitfield(current_instruction, 3, 10)
                op2 = _extract_bitfield(current_instruction, 8)
                if fn == 0:
                    instruction = "bz"
                elif fn == 1:
                    instruction = "bnz"
                elif fn == 2:
                    instruction = "bc"
                elif fn == 3:
                    instruction = "bnc"
                break

            if objcode_masked == self.instructions[0]:
                fn = _extract_bitfield(current_instruction, 3, 8)
                if fn == 0:
                    instruction = "ret"
                elif fn == 1:
                    instruction = "reti"
                elif fn == 2:
                    instruction = "enai"
                elif fn == 3:
                    instruction = "disi"
                elif fn == 4:
                    instruction = "wait"
                elif fn == 5:
                    instruction = "stby"
                break

        result = INSTR(instruction, fn, rd, op1, op2, access)
        return result
