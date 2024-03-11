'''https://adventofcode.com/2023/day/8'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import math
import re
import sys
from dataclasses import dataclass
from typing import Self

@dataclass
class Loop:
    start_index: int
    loop_length: int
    end_nodes_indexes: list[int]

def get_loop_end_nodes_coefficient(loop: Loop) -> int | None:
    if not loop.end_nodes_indexes:
        return None

    if loop.loop_length != loop.end_nodes_indexes[-1]:
        return None

    coefficient = loop.end_nodes_indexes[0]
    if all(
        node_index == (n+1) * coefficient
        for n, node_index in enumerate(loop.end_nodes_indexes)
    ):
        return coefficient
    return None


@dataclass
class Node:
    node_id: str
    left: str
    right: str

    @classmethod
    def from_string(cls, string: str) -> Self:
        match = re.search(r'(\w+) = \((\w+), (\w+)\)', string)
        if not match:
            raise ValueError(f'{string=} is not a valid string for a Node!')
        return cls(
            node_id=match.group(1),
            left=match.group(2),
            right=match.group(3)
        )

@dataclass
class Network:
    instructions: str
    nodes: dict[str, Node]

    @classmethod
    def from_string(cls, string: str) -> Self:
        instructions, node_lines = string.strip().split('\n\n')

        nodes = {}
        for node_line in node_lines.splitlines():
            node = Node.from_string(node_line)
            nodes[node.node_id] = node

        return cls(instructions=instructions, nodes=nodes)

    def travel(self, start_node_id: str, end_node_id: str) -> int:
        if start_node_id not in self.nodes:
            raise ValueError(f'Node {start_node_id} is not in the network!')
        if end_node_id not in self.nodes:
            raise ValueError(f'Node {end_node_id} is not in the network!')

        steps = 0
        current_node = self.nodes[start_node_id]
        already_visited = set()

        while current_node.node_id != end_node_id:

            visit_key = (current_node.node_id, steps % len(self.instructions))
            if visit_key in already_visited:
                raise ValueError(f'I am lost! {already_visited} -> {visit_key}')
            already_visited.add(visit_key)

            instruction = self.instructions[steps % len(self.instructions)]
            if instruction == 'L':
                current_node = self.nodes[current_node.left]
            elif instruction == 'R':
                current_node = self.nodes[current_node.right]

            steps += 1

        return steps

    def ghost_travel(self, start_nodes_tail: str, end_nodes_tail: str) -> int:

        starting_nodes_ids = [
            node_id for node_id in self.nodes.keys()
            if node_id[-1] == start_nodes_tail
        ]
        if not starting_nodes_ids:
            raise ValueError(
                f'There are no nodes starting with {start_nodes_tail}'
            )
        if not any(
            node_id[-1] == end_nodes_tail for node_id in self.nodes.keys()
        ):
            raise ValueError(
                f'There are no nodes ending with {end_nodes_tail}'
            )

        steps = 0
        current_nodes = [self.nodes[node_id] for node_id in starting_nodes_ids]

        while True:

            if all(
                node.node_id[-1] == end_nodes_tail for node in current_nodes
            ):
                return steps

            instruction = self.instructions[steps % len(self.instructions)]

            next_nodes = []
            for current_node in current_nodes:

                if instruction == 'L':
                    next_node = self.nodes[current_node.left]
                elif instruction == 'R':
                    next_node = self.nodes[current_node.right]
                else:
                    raise ValueError(f'Invalid instruction: {instruction}')

                next_nodes.append(next_node)

            current_nodes = next_nodes
            steps += 1

    def ghost_travel_with_LCM( # pylint: disable=invalid-name
        self, start_nodes_tail: str, end_nodes_tail: str
    ) -> int:

        # If for all the ghost paths, all the End nodes of each one are
        # multiples of a number, then the first encounter can be found
        # by calculating the LCM of those numbers

        starting_nodes_ids = [
            node_id for node_id in self.nodes.keys()
            if node_id[-1] == start_nodes_tail
        ]
        if not starting_nodes_ids:
            raise ValueError(
                f'There are no nodes starting with {start_nodes_tail}'
            )
        if not any(
            node_id[-1] == end_nodes_tail for node_id in self.nodes.keys()
        ):
            raise ValueError(
                f'There are no nodes ending with {end_nodes_tail}'
            )

        loops = [
            self.get_loop(node, end_nodes_tail) for node in starting_nodes_ids
        ]
        loop_coefficients = [
            get_loop_end_nodes_coefficient(loop) for loop in loops
        ]
        if not all(loop_coefficients):
            raise ValueError('Not possible to use LCM to calculate the steps')

        return math.lcm(*loop_coefficients) # type: ignore

    def get_loop(self, start_node_id: str, end_nodes_tail: str = 'Z') -> Loop:
        start = None
        steps = 0
        end_nodes_indexes = []

        current_node = self.nodes[start_node_id]

        visited = {}
        while True:
            visit_key = (current_node.node_id, steps % len(self.instructions))
            start = visited.get(visit_key)
            if start is not None:
                break
            visited[visit_key] = steps

            if current_node.node_id.endswith(end_nodes_tail):
                end_nodes_indexes.append(steps)

            instruction = self.instructions[steps % len(self.instructions)]
            current_node = (
                self.nodes[current_node.left]
                if instruction == 'L'
                else self.nodes[current_node.right]
            )
            steps += 1

        return Loop(
            start_index=start,
            loop_length=steps - start,
            end_nodes_indexes=end_nodes_indexes
        )

def main(input_text: str):
    network = Network.from_string(input_text)
    steps = network.travel(start_node_id='AAA', end_node_id='ZZZ')
    print(f'Solution part 1: {steps=}')

    # ghost_steps = network.ghost_travel('A', 'Z')
    ghost_steps = network.ghost_travel_with_LCM('A', 'Z')
    print(f'Solution part 2: {ghost_steps=}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
