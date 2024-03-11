# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest

from advent_of_code_23.day20 import (
    Pulse, BroadcastModule, FlipFlopModule, ConjuctionModule,
    Circuit, multiple_pushes

)

@pytest.fixture(name='example_configuration_one')
def example_configuration_one_fixture():
    return (
        'broadcaster -> a, b, c\n'
        '%a -> b\n'
        '%b -> c\n'
        '%c -> inv\n'
        '&inv -> a'
    )

@pytest.fixture(name='example_configuration_two')
def example_configuration_two_fixture():
    return (
        'broadcaster -> a\n'
        '%a -> inv, con\n'
        '&inv -> b\n'
        '%b -> con\n'
        '&con -> output'
    )

def test_pulse():

    pulse = Pulse(level=1, origin='button', destination='broadcaster')

    assert pulse

def test_broadcast_module():

    module = BroadcastModule(module_id='broadcaster', outputs=['a', 'b', 'c'])
    input_pulse_high = Pulse(1, 'button', 'broadcaster')
    input_pulse_low = Pulse(0, 'button', 'broadcaster')

    output_pulses_high = module.receive_pulse(input_pulse_high)
    assert output_pulses_high == [
        Pulse(1, 'broadcaster', 'a'),
        Pulse(1, 'broadcaster', 'b'),
        Pulse(1, 'broadcaster', 'c'),
    ]

    output_pulses_low = module.receive_pulse(input_pulse_low)
    assert output_pulses_low == [
        Pulse(0, 'broadcaster', 'a'),
        Pulse(0, 'broadcaster', 'b'),
        Pulse(0, 'broadcaster', 'c'),
    ]

def test_flip_flop_module():


    module = FlipFlopModule(module_id='flipflop', outputs=['a', 'b', 'c'])

    assert module.cached_level == 0

    input_pulse_high = Pulse(1, 'button', 'flipflop')
    input_pulse_low = Pulse(0, 'button', 'flipflop')

    output_pulses_high = module.receive_pulse(input_pulse_high)
    assert output_pulses_high == []
    assert module.cached_level == 0

    output_pulses_low = module.receive_pulse(input_pulse_low)
    assert output_pulses_low == [
        Pulse(1, 'flipflop', 'a'),
        Pulse(1, 'flipflop', 'b'),
        Pulse(1, 'flipflop', 'c'),
    ]
    assert module.cached_level == 1

    output_pulses_low = module.receive_pulse(input_pulse_low)
    assert output_pulses_low == [
        Pulse(0, 'flipflop', 'a'),
        Pulse(0, 'flipflop', 'b'),
        Pulse(0, 'flipflop', 'c'),
    ]
    assert module.cached_level == 0

def test_conjunction_module():

    module = ConjuctionModule(
        module_id='conjunction',
        outputs=['a', 'b', 'c'],
        memory={'previous': 1}
    )

    assert len(module.memory) == 1

    module.add_input('button')
    assert module.memory['button'] == 0

    input_pulse_high = Pulse(1, 'button', 'conjunction')
    input_pulse_low = Pulse(0, 'button', 'conjunction')

    output_pulses_high = module.receive_pulse(input_pulse_high)
    assert output_pulses_high == [
        Pulse(0, 'conjunction', 'a'),
        Pulse(0, 'conjunction', 'b'),
        Pulse(0, 'conjunction', 'c'),
    ]
    assert module.memory['button'] == 1

    output_pulses_low = module.receive_pulse(input_pulse_low)
    assert output_pulses_low == [
        Pulse(1, 'conjunction', 'a'),
        Pulse(1, 'conjunction', 'b'),
        Pulse(1, 'conjunction', 'c'),
    ]
    assert module.memory['button'] == 0

def test_circuit(example_configuration_one):

    circuit = Circuit.from_string(example_configuration_one)

    assert len(circuit.modules) == 5
    assert circuit.modules['broadcaster'] == BroadcastModule(
        'broadcaster', ['a', 'b', 'c']
    )
    assert circuit.modules['a'] == FlipFlopModule('a', ['b'])
    assert circuit.modules['b'] == FlipFlopModule('b', ['c'])
    assert circuit.modules['c'] == FlipFlopModule('c', ['inv'])
    assert circuit.modules['inv'] == ConjuctionModule(
        'inv', ['a']
    ).add_input('c')

def test_circuit_push_button(example_configuration_one):

    circuit = Circuit.from_string(example_configuration_one)

    sent_pulses = circuit.push_button()

    assert circuit == Circuit.from_string(example_configuration_one)
    low_pulses = [pulse for pulse in sent_pulses if not pulse.level]
    high_pulses = [pulse for pulse in sent_pulses if pulse.level]
    assert len(low_pulses) == 8
    assert len(high_pulses) == 4

def test_circuit_push_button_example_two(example_configuration_two):

    circuit = Circuit.from_string(example_configuration_two)

    sent_pulses = []
    sent_pulses.extend(circuit.push_button())
    sent_pulses.extend(circuit.push_button())
    sent_pulses.extend(circuit.push_button())
    sent_pulses.extend(circuit.push_button())

    low_pulses = [pulse for pulse in sent_pulses if not pulse.level]
    high_pulses = [pulse for pulse in sent_pulses if pulse.level]
    assert len(low_pulses) == 17
    assert len(high_pulses) == 11


def test_multiple_pushes_one(example_configuration_one):

    circuit = Circuit.from_string(example_configuration_one)

    sent_pulses = multiple_pushes(circuit, pushes=1000)

    low_pulses = [pulse for pulse in sent_pulses if not pulse.level]
    high_pulses = [pulse for pulse in sent_pulses if pulse.level]
    assert len(low_pulses) == 8000
    assert len(high_pulses) == 4000

def test_multiple_pushes_two(example_configuration_two):

    circuit = Circuit.from_string(example_configuration_two)

    sent_pulses = multiple_pushes(circuit, pushes=1000)

    low_pulses = [pulse for pulse in sent_pulses if not pulse.level]
    high_pulses = [pulse for pulse in sent_pulses if pulse.level]
    assert len(low_pulses) == 4250
    assert len(high_pulses) == 2750
