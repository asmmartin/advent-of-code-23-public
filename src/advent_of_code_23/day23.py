'''https://adventofcode.com/2023/day/23'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

class Direction(complex, Enum):
    UP = -1j
    DOWN = 1j
    LEFT = -1
    RIGHT = 1

@dataclass
class Node:
    coords: complex
    edges: dict[complex, int] = field(default_factory=dict)

@dataclass
class HikingMap:
    nodes: dict[complex, Node]
    start: Node
    end: Node

    @classmethod
    def from_string(cls, text: str, slippery: bool = True) -> Self:

        map_lines = text.strip().splitlines()
        height = len(map_lines)
        width = len(map_lines[0])

        start, end = None, None
        for col in range(len(map_lines[0])):
            if map_lines[0][col] == '.':
                start = col + 0j
            if map_lines[-1][col] == '.':
                end = col + (height - 1) * 1j
        if start is None or end is None:
            raise ValueError("Couldn't determine start and/or end")

        allowed_directions: dict[str, list[Direction]] = {
            '#': [], '.': list(Direction),
            '>': [Direction.RIGHT], '<': [Direction.LEFT],
            'v': [Direction.DOWN], '^': [Direction.UP]
        }
        if not slippery:
            for tile_type in '><^v':
                allowed_directions[tile_type] = list(Direction)

        # Find nodes using DFS
        node_coords_to_explore = []
        node_coords_to_explore.append(start)
        explored_nodes = {}
        while node_coords_to_explore:
            node_coords = node_coords_to_explore.pop()

            if node_coords in explored_nodes:
                continue

            node = Node(node_coords)

            # Find adjacent nodes using DFS
            tiles_to_visit = []
            tiles_to_visit.append((node_coords, 0))
            visited = set()
            while tiles_to_visit:
                tile, distance = tiles_to_visit.pop()

                if tile in visited:
                    continue
                visited.add(tile)

                # Count neighbours to determine if it is a node or not
                neighbours: list[complex] = []
                tile_label = map_lines[int(tile.imag)][int(tile.real)]
                for direction in allowed_directions[tile_label]:
                    neighbour = tile + direction
                    if not 0 <= neighbour.real < width:
                        continue
                    if not 0 <= neighbour.imag < height:
                        continue
                    if map_lines[int(neighbour.imag)][int(neighbour.real)] == '#':
                        continue

                    neighbours.append(neighbour)

                is_node = len(neighbours) > 2 or tile in (start, end)
                if is_node and distance:
                    node.edges[tile] = distance
                    if tile not in explored_nodes:
                        node_coords_to_explore.append(tile)
                    continue

                # Else, it is part of the path, continue searching
                for neighbour in neighbours:
                    if neighbour in visited:
                        continue
                    tiles_to_visit.append((neighbour, distance + 1))

            explored_nodes[node_coords] = node

        return cls(
            nodes=explored_nodes,
            start=explored_nodes[start],
            end=explored_nodes[end]
        )

    def find_longest_path(self) -> tuple[list[complex], int]:
        longest_distance = -float('inf')
        longest_path = []

        to_visit = []
        to_visit.append(([self.start.coords], 0))

        while to_visit:
            path, current_distance = to_visit.pop()
            current_tile = path[-1]

            if current_tile == self.end.coords:
                if current_distance > longest_distance:
                    longest_distance = current_distance
                    longest_path = path
                continue

            for neighbour, distance in self.nodes[current_tile].edges.items():
                if neighbour in path:
                    continue
                to_visit.append(
                    (path + [neighbour], current_distance + distance)
                )


        if longest_distance == -float('inf'):
            raise ValueError('Path not found!')
        return longest_path, int(longest_distance)

def main(input_text: str):
    hiking_map = HikingMap.from_string(input_text)
    _, distance = hiking_map.find_longest_path()
    print(f'Solution part 1: {distance}')

    non_slippery_hiking_map = HikingMap.from_string(input_text, False)
    _, distance = non_slippery_hiking_map.find_longest_path()
    print(f'Solution part 2: {distance}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
