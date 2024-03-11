'''https://adventofcode.com/2023/day/19'''

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import sys
import re
from copy import copy
from dataclasses import dataclass
from typing import Self

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_string(cls, text: str) -> Self:

        scores = re.findall(r'([xmas]=\d+)', text)
        if len(scores) != 4:
            raise ValueError(f'Invalid text: {text}')

        ratings = {}
        for score in scores:
            category, rating = score.split('=')
            ratings[category] = int(rating)

        return cls(**ratings)

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s

class Rule:

    def __init__(
        self,
        result: str,
        category: str | None = None,
        operator: str | None = None,
        amount: int | None = None,
    ) -> None:
        self.result = result
        self.category = category
        self.operator = operator
        self.amount = amount

        if operator and (category is None or amount is None):
            raise ValueError('Invalid rule!')

    def __call__(self, part: Part) -> str | None:
        if self.operator is None:
            return self.result

        if self.operator == '<':
            if getattr(part, self.category) < self.amount: # type: ignore
                return self.result
            return None
        if self.operator == '>':
            if getattr(part, self.category) > self.amount: # type: ignore
                return self.result
            return None

        raise ValueError(f'Unknown operator: {self.operator!r}')

    @classmethod
    def from_string(cls, text: str) -> Self:

        rule_match = re.match(r'([xmas])([<>])(\d+):(\w+)', text)
        if not rule_match:
            return cls(result=text)

        category, operator, amount, result = rule_match.groups()
        amount = int(amount)

        return cls(
            result=result,
            category=category,
            operator=operator,
            amount=amount
        )

@dataclass
class CategoryRanges:
    x: range
    m: range
    a: range
    s: range

    @property
    def combinations(self) -> int:
        return len(self.x) * len(self.m) * len(self.a) * len(self.s)

    def split(self, rule: Rule) -> tuple[Self, Self]:
        if rule.operator is None:
            return self, self.__class__(*(range(0),)*4)

        if rule.category is None or rule.amount is None:
            raise ValueError('Invalid rule!')

        included, excluded = copy(self), copy(self)
        current = getattr(self, rule.category)
        if rule.operator == '<':
            in_range = range(current.start, min(current.stop, rule.amount))
            out_range = range(max(rule.amount, current.start), current.stop)
        elif rule.operator == '>':
            in_range = range(max(rule.amount+1, current.start), current.stop)
            out_range = range(current.start, min(current.stop, rule.amount+1))
        else:
            raise ValueError(f'Unknown operator: {rule.operator!r}')

        in_range = in_range if in_range else range(0)
        out_range = out_range if out_range else range(0)

        setattr(included, rule.category, in_range)
        setattr(excluded, rule.category, out_range)
        return included, excluded

@dataclass
class Workflow:

    workflow_id: str
    rules: list[Rule]

    @classmethod
    def from_string(cls, text: str) -> Self:

        workflow_id, rule_texts = text.strip().split('{')
        rule_texts = rule_texts[:-1].split(',')

        rules = [Rule.from_string(rule_text) for rule_text in rule_texts]

        return cls(workflow_id=workflow_id, rules=rules)

    def evaluate_part(self, part: Part) -> str:

        for rule in self.rules:
            if (result := rule(part)):
                return result

        raise ValueError(
            f'Workflow {self.workflow_id} does not know what to do with {part=}'
        )

class OrganizationSystem:

    def __init__(self, workflows: list[Workflow]) -> None:
        self.workflows = {
            workflow.workflow_id: workflow for workflow in workflows
        }

    def evaluate_part(self, part: Part, start: str = 'in') -> str:

        current_result = start
        already_evaluated_workflows = set() # To avoid endless loops

        while current_result not in ('A', 'R'):
            if current_result in already_evaluated_workflows:
                raise ValueError('Endless loop detected!')

            already_evaluated_workflows.add(current_result)

            current_result = self.workflows[current_result].evaluate_part(part)

        return current_result

    def count_combinations(
        self, workflow_id: str, ranges: CategoryRanges
    ) -> int:

        if workflow_id == 'A':
            return ranges.combinations
        if workflow_id == 'R':
            return 0

        total_count = 0
        for rule in self.workflows[workflow_id].rules:
            if not ranges.combinations:
                break
            matched, ranges = ranges.split(rule)
            total_count += self.count_combinations(rule.result, matched)

        return total_count

def main(input_text: str):
    workflows_texts, parts_texts = input_text.strip().split('\n\n')

    workflows = [
        Workflow.from_string(text)
        for text in workflows_texts.strip().splitlines()
    ]
    parts = [
        Part.from_string(text)
        for text in parts_texts.strip().splitlines()
    ]
    system = OrganizationSystem(workflows)

    total = sum(
        part.value if system.evaluate_part(part) == 'A' else 0
        for part in parts
    )
    print(f'Solution part 1: {total}')

    ranges = CategoryRanges(*(range(1, 4001) for _ in range(4)))
    combinations = system.count_combinations('in', ranges)
    print(f'Solution part 2: {combinations}')

if __name__ == "__main__":
    INPUT_TEXT = sys.stdin.read()
    main(INPUT_TEXT)
