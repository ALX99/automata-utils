"""This module contains operations on automatons"""
import random
import string
from typing import Callable, Dict, List, Pattern, Set, Tuple

from tabulate import PRESERVE_WHITESPACE, tabulate

from lib.automaton import Automaton
from lib.cfg import CFG, Productions
from lib.dfa import DFA
from lib.state import combine_states


def verify_against_regex(
        automaton: Automaton, regex: Pattern[str],
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


def verify_against_method(
        automaton: Automaton, func: Callable[[str],
                                             int],
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


def create_distinguishability_table(dfa: DFA, show_table: bool = False,
                                    show_names: bool = True) -> Dict[int,
                                                                     Dict[int, str]]:
    # Sort the ids to create a nice looking table
    if not dfa.check_complete():
        raise ValueError("DFA needs a trap state")

    sorted_ids = [k for k in dfa.states]
    sorted_ids.sort()

    dict_table = dict(dict())
    # First iteration
    for i, id1 in enumerate(sorted_ids):
        dict_table[id1] = dict()
        for id2 in sorted_ids[:i]:
            # Check if the states differ and if they do add an X
            dict_table[id1][id2] = ("X"if dfa.states.get(
                id1).final != dfa.states.get(id2).final else "")

    # Second iteration
    # This can be done in the loop above but this way
    # makes it more clear what is going on
    found = True
    while found:
        found = False
        for id1, v1 in dict_table.items():
            for id2 in {k: v for k, v in v1.items() if v != "X"}:
                for symbol in dfa.alphabet:
                    id1_new = dfa.get_transition(id1, symbol).id
                    id2_new = dfa.get_transition(id2, symbol).id
                    if dict_table.get(id1_new).get(id2_new) == "X" or dict_table.get(id2_new).get(id1_new):
                        dict_table[id1][id2] = "X"
                        found = True

    if show_table:
        # Convert to list
        table_lists = [[dfa.states.get(id1).name if show_names else id1]
                       for id1 in sorted_ids]
        for i, id1 in enumerate(sorted_ids):
            for id2 in sorted_ids[:i]:
                table_lists[i].append(dict_table.get(id1).get(id2))
        # Create headers
        headers = [dfa.states.get(i).name if show_names else str(i)
                   for i in sorted_ids]
        headers.insert(0, "S")
        print(tabulate(table_lists, headers=headers))
    return dict_table


def product_construction(dfa1: DFA, dfa2: DFA) -> DFA:
    # Make sure they operate over the same alphabet
    if dfa1.alphabet.difference(dfa2.alphabet) != dfa1.alphabet:
        raise ValueError("The alphabets of the automatons differ")

    initial_state = combine_states(
        dfa1.initial_state, dfa2 .initial_state, dfa1.initial_state.final or dfa2.initial_state.final)

    # todo not done
    return None


def convert_to_chomsky(cfg: CFG, show_steps=False) -> CFG:
    if show_steps:
        print("Entering the bin method")
    show_steps = False
    no_bin_CFG = bin(cfg, show_steps)
    print(no_bin_CFG)


def bin(cfg: CFG, show_steps: bool) -> CFG:
    productions = cfg.get_productions()
    variables = cfg.get_variables()

    new_productions = Productions()
    for head, tail in productions.items():
        i = 0
        while i < len(tail):
            if len(tail[i]) <= 2:
                if show_steps:
                    print(f"{head} -> {tail[i]} is already valid")
                new_productions.add_production(head, tail[i])
                i += 1
                continue

            if show_steps:
                print(f"{head} -> {tail[i]} is too large")
            var = head
            j = 0
            new_var = "A"

            # When this loop finishes there will be 2
            # variables (or terminals) left
            while j < len(tail[i])-2:
                # Find a new variable that already isn't in variables
                while new_var in variables:
                    new_var = chr((ord(new_var)+1-65) % 26+65)
                new_tail = tail[i][j] + new_var
                if show_steps:
                    print(f"Creating a new production {var} -> {new_tail}")
                new_productions.add_production(var, new_tail)

                variables.add(new_var)
                # Set the new variable to the old variable
                var = new_var
                j += 1

            # Get last two variables (or terminals) from the tail
            new_tail = tail[i][j] + tail[i][j+1]
            if show_steps:
                print(f"Creating the last production {new_var} -> {new_tail}")
            new_productions.add_production(new_var, new_tail)
            i += 1

    return CFG(new_productions)


def dell():
    pass
