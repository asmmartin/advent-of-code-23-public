'''https://adventofcode.com/2023/day/20'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from dataclasses import dataclass, field
from typing import Literal, Self

@dataclass
class Pulse:
    level: Literal[0, 1]
    origin: str
    destination: str

@dataclass
class Module:
    module_id: str
    outputs: list[str]

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        raise NotImplementedError()

@dataclass
class BroadcastModule(Module):

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.destination != self.module_id:
            return []
        return [
            Pulse(pulse.level, self.module_id, destination)
            for destination in self.outputs
        ]

@dataclass
class FlipFlopModule(Module):
    cached_level: int = 0

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.destination != self.module_id:
            return []
        if pulse.level == 1:
            return []
        self.cached_level = 0 if self.cached_level else 1
        return [
            Pulse(self.cached_level, self.module_id, destination)
            for destination in self.outputs
        ]

@dataclass
class ConjuctionModule(Module):
    memory: dict[str, int] = field(default_factory=dict)

    def add_input(self, input_id: str) -> Self:
        self.memory[input_id] = 0
        return self

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.destination != self.module_id:
            return []

        if pulse.origin in self.memory:
            self.memory[pulse.origin] = pulse.level

        output_level = 1 if 0 in self.memory.values() else 0
        return [
            Pulse(output_level, self.module_id, destination)
            for destination in self.outputs
        ]

@dataclass
class Circuit:
    modules: dict[str, Module]

    @classmethod
    def from_string(cls, text: str) -> Self:
        lines = text.strip().splitlines()

        modules: dict[str, Module] = {}
        conjuction_modules: dict[str, ConjuctionModule] = {}

        for line in lines:
            module_info, outputs_text = line.split(' -> ')
            outputs = [output.strip() for output in outputs_text.split(',')]
            if module_info[0] == '%':
                module = FlipFlopModule(module_info[1:], outputs)
            elif module_info[0] == '&':
                module = ConjuctionModule(module_info[1:], outputs)
                conjuction_modules[module.module_id] = module
            else:
                module = BroadcastModule(module_info, outputs)
            modules[module.module_id] = module

        for module in modules.values():
            for output in module.outputs:
                try:
                    conjuction_modules[output].add_input(module.module_id)
                except KeyError:
                    pass

        return cls(modules=modules)

    def push_button(self) -> list[Pulse]:
        sent_pulses = [Pulse(0, 'button', 'broadcaster')]
        pulse_index = 0

        while pulse_index < len(sent_pulses):
            pulse = sent_pulses[pulse_index]
            module = self.modules.get(pulse.destination)
            if module:
                sent_pulses.extend(module.receive_pulse(pulse))
            pulse_index += 1
        return sent_pulses

def multiple_pushes(circuit: Circuit, pushes: int) -> list[Pulse]:
    sent_pulses = []
    for _ in range(pushes):
        sent_pulses.extend(circuit.push_button())
    return sent_pulses


def main(input_text: str):
    circuit = Circuit.from_string(input_text)
    sent_pulses = multiple_pushes(circuit, pushes=10_000)
    low_pulses = [pulse for pulse in sent_pulses if not pulse.level]
    high_pulses = [pulse for pulse in sent_pulses if pulse.level]
    print(f'Solution part 1: {len(low_pulses) * len(high_pulses)}')

    # Part 2 particular solution
    circuit = Circuit.from_string(input_text)
    out_nand_module = None
    for module in circuit.modules.values():
        if 'rx' in module.outputs:
            out_nand_module = module
            break
    if not out_nand_module:
        raise ValueError('No rx!!')

    dependency_highs = {
        dependency: []
        for dependency in out_nand_module.memory # type: ignore
    }
    for push_count in range(100_000):
        pulses = circuit.push_button()
        for dependency in dependency_highs:
            for pulse in pulses:
                if pulse.level and pulse.origin == dependency:
                    dependency_highs[pulse.origin].append(push_count)
                    break

    lcm = 1
    for dependency, pushes in dependency_highs.items():
        differences = [pushes[i] - pushes[i-1] for i in range(1, len(pushes))]
        if len(set(differences)) != 1:
            raise ValueError(f'Loop not found for module {dependency}!')
        lcm *= differences[0]
    print(f'Solution part 2: {lcm}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
