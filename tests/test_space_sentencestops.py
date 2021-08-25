
import os
import sys
import pytest

root = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(root)

# pylint: disable=import-error
import textstada

def msg(t, e, r):
    return f"\nTested:   '{t}'\nExpected: '{e}'\nReceived: '{r}'\n"

def run_test(func, tests):
    for test, expected in tests:
        output = func(test)
        assert output == expected, msg(test, expected, output)

def run_list_test(func, tests):
    # Test lists as inputs
    test = [i[0] for i in tests]
    expected = [i[1] for i in tests]
    output = func(test)
    assert output == expected, msg(test, expected, output)


def test_single_space():
    tests = [
        ('hello  world', 'hello world'),
        ('hello   world', 'hello world'),
        (' hello world ', 'hello world'),
        (' hello world', 'hello world'),
        ('hello  world ', 'hello world')
    ]
    f = textstada.single_space
    run_test(f, tests)
    run_list_test(f, tests)


def test_space_sentencestops():
    tests = [
        ('Bad stop.Good stop.', 'Bad stop. Good stop.'),
        ('Bad stop   .. Good stop.', 'Bad stop.. Good stop.'),
        ('100.00', '100.00'),
        ('hello .  world.', 'hello.  world.')
        ]
    f = textstada.space_sentencestops
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_numerical_commas():
    tests = [
        ('1,000,000', '1000000'),
        ('100,0', '1000'),
        ('123,456.00', '123456.00')
    ]
    f = textstada.remove_numerical_commas
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_dashes():
    tests = [
        ('COVID-19', 'COVID19'),
        ('one-to-one', 'one-to-one'),
        ('5-10', '5-10'),
        ('hello - world', 'hello  world'),
        ('hello - - world', 'hello   world'),
        ('hello -  - world', 'hello    world'),
        ('hello-  world', 'hello-  world'),
        ('hello  – - world', 'hello    world'),
        ('- hello world', ' hello world'),
        ('1-to-1', '1-to-1')
    ]
    f = textstada.remove_dashes
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_bullets():
    tests = [
        ('• hello world', 'hello world'),
        (' • hello world', 'hello world'),
        ('• hello world  • hello world', 'hello world. hello world')
    ]
    f = textstada.remove_bullets
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_escapes():
    tests = [
        (r' \n hello world \n hello world', 'hello world. hello world'),
        (r'\r hello world \t', 'hello world.'),
    ]
    f = textstada.remove_escapes
    run_test(f, tests)
    run_list_test(f, tests)


def test_add_fullstop():
    tests = [
        ('hello world', 'hello world.'),
        ('hello world.', 'hello world.'),
        ('hello world ', 'hello world.'),
        ('hello world. ', 'hello world.'),
        ('hello world?', 'hello world?'),
        ('hello world;::', 'hello world.'),
        ('hello world!;::', 'hello world!'),
        ('hello world - ', 'hello world.')
        ]
    f = textstada.add_fullstop
    run_test(f, tests)
    run_list_test(f, tests)


# def test_replace_contractions():
#     tests = [
#         (r"I shouldn't have", "I should not have"),
#         (r"who'd be", "who would be"),
#         (r"wouldn't've", "would not have")
#         ]
#     f = textstada.replace_contractions
#     run_test(f, tests)
#     run_list_test(f, tests)

