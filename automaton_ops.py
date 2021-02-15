import random
from typing import Callable, Pattern

from automaton import Automaton
from dfa import DFA
from state import combine_states


def verify_against_regex(automaton: Automaton, regex: Pattern[str],
                         test_num: int = 10000, max_sample_num: int = 12) -> bool:
    """Verifies the automaton against a regex

    Args:
        automaton (Automaton): The automaton to test
        regex (Pattern[str]): The regex to compare it with
        test_num (int, optional): The number of tests. Defaults to 10000.
        sample_num (int, optional): The number of symbols to construct tests from. Defaults to 12.

    Returns:
        bool: True if they match
    """
    symbols = list(automaton.alphabet)

    for i in range(1, max_sample_num):
        print(f"\rTesting with sample size {i}", end="")
        for _ in range(test_num):
            test = "".join([random.choice(symbols) for _ in range(i)])
            if regex.match(test):
                if not automaton.check_string_in_language(test):
                    print(f"\nRegex matched on {test} and automaton didn't")
                    return False
            else:
                if automaton.check_string_in_language(test):
                    print(f"\nRegex didn't match on {test} and automaton did")
                    return False
    return True


def verify_against_method(automaton: Automaton, func: Callable[[str], int],
                          test_num: int = 10000, max_sample_num: int = 12) -> bool:
    """Verifies the automaton against a method

    Args:
        automaton (Automaton): The automaton to test
        func (Callable[[str], int]): The method to check against
        test_num (int, optional): The number of tests. Defaults to 10000.
        max_sample_num (int, optional): The number of symbols to construct tests from. Defaults to 12.

    Returns:
        bool: True if they match
    """
    symbols = list(automaton.alphabet)

    for i in range(1, max_sample_num):
        print(f"\rTesting with sample size {i}", end="")
        for _ in range(test_num):
            test = "".join([random.choice(symbols) for _ in range(i)])
            if func(test):
                if not automaton.check_string_in_language(test):
                    print(f"\nMethod matched on {test} and automaton didn't")
                    return False
            else:
                if automaton.check_string_in_language(test):
                    print(f"\nMethod didn't match on {test} and automaton did")
                    return False
    return True


def product_construction(a1: DFA, a2: DFA) -> DFA:
    # Make sure they operate over the same alphabet
    if a1.alphabet.difference(a2.alphabet) != a1.alphabet:
        raise ValueError("The alphabets of the automatons differ")

    initial_state = combine_states(a1.initial_state, a2
                                   .initial_state, a1.initial_state.final or a2.initial_state.final)

    # todo not done
    return None
