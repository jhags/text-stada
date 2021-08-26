
import pytest

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


def test_replace_contractions():
    tests = [
        (r"I shouldn't have", "I should not have"),
        (r"who'd be", "who would be"),
        (r"wouldn't've", "would not have"),
        (r"dont be silly", "do not be silly")
        ]
    f = textstada.replace_contractions
    run_test(f, tests)
    run_list_test(f, tests)


def test_clean_quote_chars():
    tests = [
        (r"‘Some bad quote’ and apos´s", "'Some bad quote' and apos's"),
        (r"“Bad double quotes”", '"Bad double quotes"')
        ]
    f = textstada.clean_quote_chars
    run_test(f, tests)
    run_list_test(f, tests)


def test_replace_latin_abbrevs():
    tests = [
        ("this is e.g. edge. e. g.  be. g.", "this is eg edge. eg  be. g."),
        ("e.g.", "eg"),
        ("e.g", "eg"),
        ("I.E.", "ie")
        ]
    f = textstada.replace_latin_abbrevs
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_pronouns():
    tests = [
        ("He went", "went"),
        ("what he wanted", "what wanted"),
        ("they've needed.", "have needed.")
        ]
    f = textstada.remove_pronouns
    run_test(f, tests)
    run_list_test(f, tests)


def test_remove_punctuation():
    tests = [
        ('This is [a] "string". Hello world!', "This is a string . Hello world!"),
        ('{some} tricky/weird% (chars)', "some tricky weird% (chars)")
        ]
    f = textstada.remove_punctuation
    run_test(f, tests)
    run_list_test(f, tests)
