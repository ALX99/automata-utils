"""This module contains operations on automatons"""
import random
import re
import itertools
from typing import Callable, Dict,  Pattern

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
                    if dict_table.get(id1_new).get(id2_new) == "X" or dict_table.get(id2_new).get(
                            id1_new):
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

    initial_state = combine_states(dfa1.initial_state, dfa2 .initial_state,
                                   dfa1.initial_state.final or dfa2.initial_state.final)

    # todo not done
    return None


def convert_to_chomsky(cfg: CFG, show_steps=False) -> CFG:
    prod = cfg.get_productions()
    prod.add_production("P", cfg.get_start_state())
    new = CFG("P'", prod)

    a = bin(cfg, show_steps)
    print("== Done with bin ==")
    print(a)
    print("===================")

    b = dell(a, show_steps)
    print("== Done with del ==")
    print(b)
    print("===================")

    c = unit(b, show_steps)
    print("== Done with unit ==")
    print(c)
    print("====================")

    d = term(c, show_steps)
    print("== Done with term ==")
    print(d)
    print("====================")


def bin(cfg: CFG, show_steps: bool) -> CFG:
    variables = cfg.get_variables()
    new_productions = Productions()
    for head, tail in cfg.get_productions().items():
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

            new_head = head
            new_var = "A"
            # When this loop finishes there will be 2
            # variables (or terminals) left
            j = 0
            while j < len(tail[i])-2:
                # Find a new variable that already isn't in variables
                while new_var in variables:
                    new_var = chr((ord(new_var)+1-65) % 26+65)
                new_tail = tail[i][j] + new_var
                if show_steps:
                    print(f"Creating a new production {new_head} -> {new_tail}")
                new_productions.add_production(new_head, new_tail)

                variables.add(new_var)
                # Set the new variable to the old variable
                new_head = new_var
                j += 1

            # Get last two variables (or terminals) from the tail
            new_tail = tail[i][j] + tail[i][j+1]
            if show_steps:
                print(f"Creating the last production {new_var} -> {new_tail}")
            new_productions.add_production(new_var, new_tail)
            i += 1

    return CFG(cfg.get_start_state(), new_productions)


def dell(cfg: CFG, show_steps: bool) -> CFG:
    new_cfg = CFG(cfg.get_start_state(), cfg.get_productions())
    # Set of nullable variables
    nullables = set()

    # Find all variables that are nullable in one step
    for head, tails in cfg.get_productions().items():
        for tail in tails:
            if tail == "!":
                if show_steps:
                    print(f"{head} -> {tail} is a nullable symbol")
                nullables.add(head)

    for nullable in nullables:
        new_cfg.remove_production(nullable, "!")
        for head, tails in new_cfg.get_dict_productions_raw().items():
            new_tails = tails.copy()
            for tail in tails:
                # Check if tail contains nullable symbol
                if tail.count(nullable) > 0:
                    if show_steps:
                        print(f"{head} -> {tail} contains nullabe symbols")

                    # Find all indexes
                    indexes = [m.start() for m in re.finditer(nullable, tail)]
                    # Get all combinations
                    for L in range(1, len(indexes)+1):
                        for subset in itertools.combinations(indexes, L):
                            listy = list(subset)
                            listy.sort()
                            new_tail = tail
                            for i, pos in enumerate(listy):
                                new_tail = new_tail[:pos-i]+new_tail[pos-i+1:]
                            if show_steps:
                                print(f"Adding {head} -> {new_tail}")
                            new_tails.append(new_tail)

            # Add the new tails found
            for new_tail in set(new_tails).difference(tails):
                tails.append(new_tail)

    return new_cfg


def unit(cfg: CFG, show_steps: bool) -> CFG:
    productions = cfg.get_productions()
    new_cfg = CFG(cfg.get_start_state(), cfg.get_productions())

    while True:
        # Find unit pairs
        unit_pairs = set()
        for head, tails in new_cfg.get_productions().items():
            for tail in tails:
                if tail in productions:
                    unit_pairs.add((head, tail))

        # Break when can't find any more unit pairs
        if len(unit_pairs) == 0:
            break

        for pair in unit_pairs:
            head, tt = pair
            new_tails = []
            # Remove the unit pair
            new_cfg.get_dict_productions_raw()[head].remove(tt)
            if show_steps:
                print(f"Removing unit pair {head} -> {tt}")

            for tail in new_cfg.get_dict_productions_raw()[tt]:
                new_tails.append(tail)
            for new_tail in new_tails:
                if show_steps:
                    print(f"Adding {head} -> {new_tail} since we had that {tt} -> {new_tail}")
                new_cfg.add_production(head, new_tail)
    # new_cfg.remove_unreachable_productions()
    return new_cfg


def term(cfg: CFG, show_steps: bool) -> CFG:
    productions = cfg.get_productions()
    variables = cfg.get_variables()
    new_productions = Productions()
    for head, tails in productions.items():
        for tail in tails:
            if len(tail) < 2 or not any([char in productions for char in tail]):
                new_productions.add_production(head, tail)
                continue
            terminals = {char for char in tail if char not in productions}
            new_tail = tail
            new_var = "A"
            for terminal in terminals:
                # Get new variable
                while new_var in variables:
                    new_var = chr((ord(new_var)+1-65) % 26+65)
                # Add nwe variable
                new_productions.add_production(new_var, terminal)
                variables.add(new_var)
                # Replace the terminal in the tail with a variable
                new_tail = new_tail.replace(terminal, new_var)
            # Finally add the new tail
            new_productions.add_production(head, new_tail)

    return CFG(cfg.get_start_state(), new_productions)
