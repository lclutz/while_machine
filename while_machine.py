#!/usr/bin/env python3

import re
import sys

from typing import Dict, List


class WhileMachine():
    def __init__(self) -> None:
        self.register: Dict[int, int] = {}
        self.programm: List[Token] = []

    def read_register(self, index: int) -> int:
        return self.register[index] if index in self.register else 0

    def write_register(self, index: int, value: int) -> None:
        self.register[index] = value

    def run(self) -> int:
        for instruction in self.programm:
            instruction.evaluate(self)
        return self.read_register(0)


class Token:
    def evaluate(self, machine: WhileMachine) -> None:
        pass


class Addition(Token):
    def __init__(self, target: int, variable: int, constant: int) -> None:
        self.target = target
        self.variable = variable
        self.constant = constant

    def evaluate(self, machine: WhileMachine) -> None:
        machine.write_register(self.target,
                               machine.read_register(self.variable) + self.constant)

    def __repr__(self) -> str:
        return f"x{self.target} := x{self.variable} + {self.constant};"


class Subtraction(Token):
    def __init__(self, target: int, variable: int, constant: int) -> None:
        self.target = target
        self.variable = variable
        self.constant = constant

    def evaluate(self, machine: WhileMachine) -> None:
        result = machine.read_register(self.variable) - self.constant
        machine.write_register(self.target, result if result >= 0 else 0)

    def __repr__(self) -> str:
        return f"x{self.target} := x{self.variable} - {self.constant};"


class Loop(Token):
    def __init__(self, test: int, instructions: List[Token]) -> None:
        self.test = test
        self.instructions = instructions

    def evaluate(self, machine: WhileMachine) -> None:
        while(machine.read_register(self.test) > 0):
            for instruction in self.instructions:
                instruction.evaluate(machine)

    def __repr__(self) -> str:
        return f"WHILE (x{self.test} > 0) DO"


class LoopEnd(Token):
    def __repr__(self) -> str:
        return "END;"


class Lexer():
    def __init__(self, source_code: str) -> None:
        source_code = source_code.split('\n')
        source_code = filter(lambda l: l != "" and l[0] != '#', source_code)
        self.source_code = re.sub("\s", "", "".join(source_code).lower())

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        if self.source_code == "":
            raise StopIteration

        match = re.match("^while\(x([0-9])+>0\)do", self.source_code)
        if match != None:
            self.source_code = self.source_code[len(match[0]):]
            return Loop(int(match[1]), [])

        match = re.match(
            "^x([0-9])+:=x([0-9])+([+,-])([0-9])+;", self.source_code)
        if match != None and match[3] == '+':
            self.source_code = self.source_code[len(match[0]):]
            return Addition(int(match[1]),
                            int(match[2]),
                            int(match[4]))

        if match != None and match[3] == '-':
            self.source_code = self.source_code[len(match[0]):]
            return Subtraction(int(match[1]),
                               int(match[2]),
                               int(match[4]))

        if re.match("^end;", self.source_code) != None:
            self.source_code = self.source_code[4:]
            return LoopEnd()

        print("[ERROR]: couldn't parse")
        print(self.source_code)
        exit(1)


def parse(lexer: Lexer) -> List[Token]:
    ret = []
    for token in lexer:
        if isinstance(token, Loop):
            token.instructions = parse(lexer)

        ret.append(token)

        if isinstance(token, LoopEnd):
            return ret

    return ret


def print_instruction(instruction: Token, indentation: int = 0) -> None:
    if isinstance(instruction, LoopEnd):
        indentation = max(0, indentation - 1)

    print(indentation * "\t" + str(instruction))
    if isinstance(instruction, Loop):
        for loop_instruction in instruction.instructions:
            print_instruction(loop_instruction, indentation + 1)


def main():
    source_code = ""
    machine = WhileMachine()

    for index, arg in enumerate(sys.argv):

        if index == 1:
            with open(arg) as file:
                source_code = file.read()

        if index > 1:
            machine.write_register(index - 1, int(arg))

    machine.programm = parse(Lexer(source_code))
    print(f"x0 = {machine.run()}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("User interrupted execution")
        exit(1)
