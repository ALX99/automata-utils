import random
from typing import Callable, Pattern

from automaton import Automaton


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
            test_string = "".join([random.choice(symbols) for _ in range(i)])
            if regex.match(test_string):
                if not automaton.check_string_in_language(test_string):
                    print(
                        f"Regex matched on {test_string} and automaton didn't")
                    return False
            else:
                if automaton.check_string_in_language(test_string):
                    print(
                        f"Regex didn't match on {test_string} and automaton did")
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
            test_string = "".join([random.choice(symbols) for _ in range(i)])
            if func(test_string):
                if not automaton.check_string_in_language(test_string):
                    print(
                        f"Regex matched on {test_string} and automaton didn't")
                    return False
            else:
                if automaton.check_string_in_language(test_string):
                    print(
                        f"Regex didn't match on {test_string} and automaton did")
                    return False
    return True
