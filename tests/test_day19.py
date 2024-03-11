# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day19 import (
    Part, Rule, Workflow, OrganizationSystem, CategoryRanges
)

@pytest.fixture(name='example_workflows_text')
def example_workflows_text_fixture():
    return (
        'px{a<2006:qkq,m>2090:A,rfg}\n'
        'pv{a>1716:R,A}\n'
        'lnx{m>1548:A,A}\n'
        'rfg{s<537:gd,x>2440:R,A}\n'
        'qs{s>3448:A,lnx}\n'
        'qkq{x<1416:A,crn}\n'
        'crn{x>2662:A,R}\n'
        'in{s<1351:px,qqz}\n'
        'qqz{s>2770:qs,m<1801:hdj,R}\n'
        'gd{a>3333:R,R}\n'
        'hdj{m>838:A,pv}'
    )


@pytest.fixture(name='example_parts_text')
def example_parts_text_fixture():
    return (
        '{x=787,m=2655,a=1222,s=2876}\n'
        '{x=1679,m=44,a=2067,s=496}\n'
        '{x=2036,m=264,a=79,s=2244}\n'
        '{x=2461,m=1339,a=466,s=291}\n'
        '{x=2127,m=1623,a=2188,s=1013}'
    )

@pytest.fixture(name='example_parts')
def example_parts_fixture(example_parts_text):
    return tuple(
        Part.from_string(line)
        for line in example_parts_text.strip().splitlines()
    )

def test_part(example_parts_text):

    parts = [
        Part.from_string(line)
        for line in example_parts_text.strip().splitlines()
    ]

    assert [part.x for part in parts] == [787, 1679, 2036, 2461, 2127]
    assert [part.m for part in parts] == [2655, 44, 264, 1339, 1623]
    assert [part.a for part in parts] == [1222, 2067, 79, 466, 2188]
    assert [part.s for part in parts] == [2876, 496, 2244, 291, 1013]

def test_part_value(example_parts):

    values = [
        example_parts[0].value, example_parts[2].value, example_parts[4].value
    ]

    assert values == [7540, 4623, 6951]

def test_rule_always_accept(example_parts):

    rule = Rule.from_string('A')

    results = [rule(part) for part in example_parts]

    assert results == ['A'] * len(example_parts)

def test_rule_always_reject(example_parts):

    rule = Rule.from_string('R')

    results = [rule(part) for part in example_parts]

    assert results == ['R'] * len(example_parts)

def test_rule_always_workflow(example_parts):

    rule = Rule.from_string('hello')

    results = [rule(part) for part in example_parts]

    assert results == ['hello'] * len(example_parts)

def test_rule_less_than(example_parts):

    texts = [
        'x<800:A', 'm<50:R', 'a<200:one', 's<300:two'
    ]

    rules = [Rule.from_string(text) for text in texts]

    assert rules[0](example_parts[0]) == 'A'
    assert rules[0](example_parts[1]) is None

    assert rules[1](example_parts[1]) == 'R'
    assert rules[1](example_parts[3]) is None

    assert rules[2](example_parts[2]) == 'one'
    assert rules[2](example_parts[1]) is None

    assert rules[3](example_parts[3]) == 'two'
    assert rules[3](example_parts[1]) is None

def test_rule_greater_than(example_parts):

    texts = [
        'x>800:A', 'm>50:R', 'a>200:one', 's>300:two'
    ]

    rules = [Rule.from_string(text) for text in texts]

    assert rules[0](example_parts[1]) == 'A'
    assert rules[0](example_parts[0]) is None

    assert rules[1](example_parts[3]) == 'R'
    assert rules[1](example_parts[1]) is None

    assert rules[2](example_parts[1]) == 'one'
    assert rules[2](example_parts[2]) is None

    assert rules[3](example_parts[1]) == 'two'
    assert rules[3](example_parts[3]) is None

def test_workflow(example_workflows_text):

    lines = example_workflows_text.strip().splitlines()
    workflow = Workflow.from_string(lines[0])

    assert workflow.workflow_id == 'px'
    assert len(workflow.rules) == 3

def test_workflow_evaluate_part(example_workflows_text, example_parts):

    lines = example_workflows_text.strip().splitlines()
    workflows = [Workflow.from_string(line) for line in lines]
    workflows = {workflow.workflow_id: workflow for workflow in workflows}

    assert workflows['in'].evaluate_part(example_parts[0]) == 'qqz'
    assert workflows['gd'].evaluate_part(example_parts[1]) == 'R'
    assert workflows['qqz'].evaluate_part(example_parts[2]) == 'hdj'
    assert workflows['px'].evaluate_part(example_parts[3]) == 'qkq'
    assert workflows['rfg'].evaluate_part(example_parts[4]) == 'A'

def test_organization_system(example_workflows_text):

    lines = example_workflows_text.strip().splitlines()
    workflows = [Workflow.from_string(line) for line in lines]

    system = OrganizationSystem(workflows=workflows)

    assert len(system.workflows) == 11

def test_organization_system_evaluate_part(
    example_workflows_text, example_parts
):

    lines = example_workflows_text.strip().splitlines()
    workflows = [Workflow.from_string(line) for line in lines]
    system = OrganizationSystem(workflows=workflows)

    evaluations = [
        system.evaluate_part(part, start='in') for part in example_parts
    ]

    assert evaluations == ['A', 'R', 'A', 'R', 'A']

def test_category_ranges():


    ranges = CategoryRanges(
        x=range(1, 11), m=range(11,21), a=range(21, 31), s=range(31, 41)
    )

    assert ranges.combinations == 10_000

def test_category_ranges_split():

    ranges = CategoryRanges(*(range(1, 11) for _ in range(4)))
    rules = [
        Rule('X', 'x', '<', 6),
        Rule('X', 'm', '>', 6),
        Rule('X', 'x', '<', 5),
        Rule('X', 'm', '<', 9),
    ]

    included, excluded = ranges.split(rules[0])
    assert included == CategoryRanges(range(1, 6), *(range(1, 11),)*3)
    assert excluded == CategoryRanges(range(6, 11), *(range(1, 11),)*3)


    included, excluded = excluded.split(rules[1])
    assert included == CategoryRanges(
        range(6, 11), range(7, 11), *(range(1, 11),)*2
    )
    assert excluded == CategoryRanges(
        range(6, 11), range(1, 7), *(range(1, 11),)*2
    )

    included, excluded = excluded.split(rules[2])
    assert included == CategoryRanges(
        range(0), range(1, 7), *(range(1, 11),)*2
    )
    assert excluded == CategoryRanges(
        range(6, 11), range(1, 7), *(range(1, 11),)*2
    )

    included, excluded = excluded.split(rules[3])
    assert included == CategoryRanges(
        range(6, 11), range(1, 7), *(range(1, 11),)*2
    )
    assert excluded == CategoryRanges(
        range(6, 11), range(0), *(range(1, 11),)*2
    )

def test_organization_system_count_combinations(example_workflows_text):

    ranges = CategoryRanges(*(range(1, 4001) for _ in range(4)))
    lines = example_workflows_text.strip().splitlines()
    workflows = [Workflow.from_string(line) for line in lines]
    system = OrganizationSystem(workflows=workflows)

    combinations_count = system.count_combinations('in', ranges)

    assert combinations_count == 167409079868000
