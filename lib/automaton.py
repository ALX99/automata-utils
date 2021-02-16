"""Module that contains common logic to automatons"""
import sys
from typing import Dict, Iterable, List, Optional, Set

from lib.state import State
from lib.transition import Transition


class Automaton:
    """Class representing an automaton"""

    def __init__(self, states: Set[State], transitions: Dict[Transition, List[int]]) -> None:
        self.initial_state: State
        self.transitions: Dict[Transition, Set[State]]
        self.transitions = dict()
        self.alphabet = set()

        # We'll convert to a dict here for faster lookup
        self.states = {state.id: state for state in states}

        # Find initial state
        for _, state in self.states.items():
            if state.initial:
                self.initial_state = state
        if self.initial_state is None:
            print("No initial state found")
            sys.exit(1)

        for transition, dests in transitions.items():
            # Get all transitions
            self.transitions[transition] = {
                self.states[dest] for dest in dests}
            # Add the strings on the transitions to the alphabet
            self.alphabet.add(transition.string)

        # Look for missing states in all transitions
        self._check_ids(
            [transition.origin for transition in self.transitions])
        self._check_ids(
            [dest.id for _, dests in self.transitions.items()for dest in dests])

    def get_transition(self, state_id: int, symbol: str) -> Optional[Set[State]]:
        return self.transitions.get(Transition(state_id, symbol))

    def _check_ids(self, ids: Iterable[int]) -> None:
        """Check that all state ids exist in the automaton

        Args:
            ids (List[int]): The list of ids

        Returns:
            bool: True if all ids exists in the automaton
        """
        if not all(id in self.states for id in ids):
            print("Missing states in automaton")
            sys.exit(1)

    def _get_symbols(self, string: str) -> List[str]:
        """Returns the symbols from a string in the right order

        Args:
            string (str): The string to get symbols from

        Returns:
            List[str]: The symbols extracted from the string
        """
        steps, start, stop = [], 0, 1

        # Don't touch this, I think it works
        while stop <= len(string):
            attempt = string[start:stop]
            while attempt in self.alphabet and stop <= len(string):
                stop += 1
                attempt = string[start:stop]

            steps.append(string[start:stop-1])
            start = stop-1
            stop += 1

        # Add the last substring
        if len(string) != 1:  # todo fix this if statement
            steps.append(string[start:stop])

        return steps

    # This method is implemented in DFA and NFA and only
    # serves # as a placeholder here
    def check_string_in_language(self, _: str) -> bool:
        """Check if a string is inside the language this DFA/NFA

        Args:
            _ (str): The string to check

        Returns:
            bool: True if the string is inside the language
        """
        return False
