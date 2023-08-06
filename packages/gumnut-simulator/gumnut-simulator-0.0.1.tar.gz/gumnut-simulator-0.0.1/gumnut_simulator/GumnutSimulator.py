from enum import IntEnum
from collections import OrderedDict
import json
import logging
from gaspy import GumnutAssembler
from gumnut_simulator import __version__
from gumnut_simulator.GumnutCore import GumnutCore
from gumnut_simulator import GumnutExceptions

logger = logging.getLogger("root")


class SimulatorState(IntEnum):
    halt = 0
    idle = 1
    breakpoint = 2


class GumnutSimulator:
    def __init__(self):
        self.CPU = GumnutCore()
        self.lsom_map = dict()
        self.lines_of_code = 0
        self.current_line = 0
        self.number_of_instructions = 0
        self.register_format = "#04x"
        self.instr_memory_format = "05x"
        self.data_memory_format = "02x"
        self.memory_format = "d"
        self.breakpoints = list()
        self.exception = None
        self.state = SimulatorState.halt
        self.asm_source = ""
        self.debug_symbols = OrderedDict()
        self.previous_PC = -1

    def reset(self):
        """Reset the Simulator and the CPU"""
        self.CPU.reset()
        self.lsom_map.clear()
        self.lines_of_code = 0
        self.number_of_instructions = 0
        self.current_line = 0
        self.breakpoints.clear()
        self.exception = None
        self.state = SimulatorState.halt
        self.asm_source = ""
        self.debug_symbols = OrderedDict()
        self.previous_PC = -1

    def setup(self, source):
        """Initialize the CPU"""
        self.reset()
        try:
            assembler = GumnutAssembler.GumnutAssembler()  # Create as a persistent member or only when needed here?
            assembler.load_asm_source(source)
            assembler.assemble()

            self.asm_source = source
            self.lsom_map = assembler.source_objectcode_map
            self.lines_of_code = assembler.ASMLineCount
            self.number_of_instructions = assembler.InstrCount / 2

            self.CPU.upload_data_memory(assembler.get_data_memory())
            self.CPU.upload_instruction_memory(assembler.get_instruction_memory())

            if self.number_of_instructions > 0:
                self.state = SimulatorState.idle
            else:
                self.state = SimulatorState.halt

            self.debug_symbols = assembler.source_objectcode_map

        except (GumnutExceptions.InvalidInstruction, GumnutExceptions.InstructionMemorySizeExceeded) as e:
            self.exception = e
            self.state = SimulatorState.halt
        else:
            return True

    def step(self):
        """Triggers a single step of the CPU"""
        try:
            self.previous_PC = self.CPU.PC
            self.CPU.step()
            if self.get_current_line() in self.breakpoints:
                self.state = SimulatorState.breakpoint
            else:
                self.state = SimulatorState.idle
        except (GumnutExceptions.InvalidInstruction, GumnutExceptions.EmptyReturnStack) as e:
            self.exception = e
            self.state = SimulatorState.halt
            return False
        except GumnutExceptions.ReturnAddressStackOverflow as e:
            self.exception = e
            self.state = SimulatorState.breakpoint
            return True
        else:
            return True

    def get_flags(self):
        """
        Return CPU flags as a dict

        :return: ``{'CARRY': False, 'ZERO': True, 'WAIT': False, 'STBY': False, 'IEN': False}``
        """

        result = dict()
        result.update({"CARRY": self.CPU.CARRY})
        result.update({"ZERO": self.CPU.ZERO})
        result.update({"WAIT": self.CPU.WAIT})
        result.update({"STBY": self.CPU.STBY})
        result.update({"IREN": self.CPU.IREN})
        return result

    def get_register(self):
        """
        Return CPU register as a dict

        :return: ``{'r0': '0x00', 'r1': '0x00', ... , 'r7': '0x00',
                    'PC': '0x00', 'SP': '0x00', 'RAS': ['F8', 'F4', 'B5', 'F7', 'C1' ]}``"""
        result = dict()

        for i in range(0, 8):
            register_name = "r" + str(i)
            result.update({register_name: self._get_formatted_number(self.CPU.r[i], self.register_format)})

        result.update({"PC": self._get_formatted_number(self.CPU.PC, "#04x")})
        result.update({"SP": self._get_formatted_number(self.CPU.SP, "#04x")})

        ras = list()
        for i in range(0, 8):
            ras.append(self._get_formatted_number(self.CPU.return_address_stack[i], "03x"))
        result.update({"RAS": ras})

        return result

    def get_instruction_memory(self, offset=0, size=4096):
        """
        Return CPU instruction memory as a list

        :return: ``['F8', 'F4', 'B5', 'F7', 'C1', '97', ... , 'D8', 'D4', '86', '94', '9B']``"""
        result = [
            self._get_formatted_number(member, self.instr_memory_format)
            for member in self.CPU.instruction_memory[offset : offset + size]
        ]
        return result

    def get_data_memory(self, offset=0, size=256):
        """
        Return CPU data memory as a list

        :return: ``['F8', 'F4', 'B5', 'F7', 'C1', '97', ... , 'D8', 'D4', '86', '94', '9B']``"""
        result = [
            self._get_formatted_number(member, self.data_memory_format)
            for member in self.CPU.data_memory[offset : offset + size]
        ]
        return result

    def get_IO_controller_register(self):
        return self.CPU.IO_controller_register

    def set_IO_controller_register(self, address, value):
        self.CPU.IO_controller_register[address] = value

    def get_current_line(self):
        """
        Return the current line number by looking up the current
        instruction memory pointer
        """
        for line_number, value in self.lsom_map.items():
            if value[3] == self.CPU.PC:
                return line_number
        return -1

    def get_simulator_data(self):
        """Return some debug/additional information"""
        result = dict()
        result.update({"state": self.state})
        result.update({"lines_of_code": self.lines_of_code})
        result.update({"number_of_instructions": self.number_of_instructions})
        result.update({"current_line": self.get_current_line()})
        result.update({"breakpoints": self.get_breakpoints()})
        result.update({"data_memory_access_addr": self.CPU.data_memory_access_addr})
        if self.CPU.instruction is not None and self.CPU.instruction.instruction == "jsb":
            current_ret_line = self._get_source_line_from_address(self.previous_PC + 1)
            result.update({"current_ret_line": current_ret_line})

        if self.exception:
            result.update({"exception": self.exception.as_dict()})
            self.exception = None
        return result

    def set_number_format(self, identifier="", number_format="d"):
        """Set number format"""
        if identifier == "register":
            if number_format == "d":
                self.register_format = "d"
            elif number_format == "h":
                self.register_format = "#04x"
            elif number_format == "o":
                self.register_format = "#05o"
            elif number_format == "b":
                self.register_format = "#010b"
        elif identifier == "memory":
            if number_format == "d":
                self.memory_format = "d"
            elif number_format == "h":
                self.memory_format = "02x"
            elif number_format == "o":
                self.memory_format = "03o"
            elif number_format == "b":
                self.memory_format = "08b"

    def _get_formatted_number(self, number, number_format):
        return format(number, number_format)

    def toggle_breakpoint(self, line_number):
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
        else:
            self.breakpoints.append(line_number)

    def get_breakpoints(self):
        return self.breakpoints

    def get_state(self):
        return self.state

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def _get_source_line_from_address(self, address):
        for line_number, field in self.debug_symbols.items():
            if field[3] == address:
                return line_number
        return -1

    def trigger_interrupt(self):
        self.CPU.IR = True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Gumnut Simulator")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
        help="show the version number and exit",
    )

    parser.parse_args()

    return 0


if __name__ == "__main__":
    main()
