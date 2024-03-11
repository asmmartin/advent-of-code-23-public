'''https://adventofcode.com/2023/day/15'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from dataclasses import dataclass
import sys

@dataclass
class Lens:
    label: str
    focal_length: int

class Box:

    def __init__(self, box_id: int, lenses: list[Lens] | None = None) -> None:
        if not lenses:
            lenses = []
        self.box_id = box_id
        self.lenses = lenses

    @property
    def focusing_powers(self) -> tuple[int, ...]:
        return tuple(
            (1 + self.box_id) * (1 + index) * lens.focal_length
            for index, lens in enumerate(self.lenses)
        )

class BoxArray:

    def __init__(self) -> None:
        self.boxes = {index: Box(box_id=index) for index in range(256)}

    def process_step(self, step: str) -> None:
        if '=' in step:
            label, focal_length = step.split('=')
            lens = Lens(label, int(focal_length))
            self.insert_lens(lens)
        elif '-' in step:
            label = step.split('-')[0]
            self.remove_lens(label)
        else:
            raise ValueError(f'Unknown {step=}')

    def insert_lens(self, new_lens: Lens):
        box = self.boxes[hash_text(new_lens.label)]

        for index, lens in enumerate(box.lenses):
            if lens.label == new_lens.label:
                box.lenses = (
                    box.lenses[:index] +
                    [new_lens] +
                    box.lenses[index+1:]
                )
                break
        else:
            box.lenses.append(new_lens)

    def remove_lens(self, label: str) -> Lens | None:

        box = self.boxes[hash_text(label)]

        for index, lens in enumerate(box.lenses):
            if lens.label == label:
                box.lenses = (
                    box.lenses[:index] +
                    box.lenses[index+1:]
                )
                return lens

def hash_text(text: str) -> int:
    value = 0

    for character in text:
        value += ord(character)
        value *= 17
        value %= 256

    return value

def main(input_text: str):
    sequence_steps = input_text.strip().replace('\n', '').split(',')
    hashes = [hash_text(step) for step in sequence_steps]
    print(f'Solution part 1: {sum(hashes)}')

    box_array = BoxArray()
    for step in sequence_steps:
        box_array.process_step(step)
    total_focusing_power = sum(
        sum(box.focusing_powers)
        for box in box_array.boxes.values()
    )
    print(f'Solution part 2: {total_focusing_power}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
