import pprint
from typing import Dict, Iterable, List, Set

from automaton import Automaton
from state import State
from transition import Transition


class NFA(Automaton):
    def __init__(self, states: Set[State], transitions: Dict[Transition, List[int]]) -> None:
        super().__init__(states, transitions)
        self.nfa_transition_table: Dict[str, List[str]]
        self.nfa_transition_table = dict()

        # Build an NFA table
        self._build_nfa_symbol_steps()

    # todo this should be on transition to transitions instead of str to strs
    def _build_nfa_symbol_steps(self) -> None:
        """Build an "nfa transition table" where if
        you encounter a symbol that is key in the nfa transition
        table dict and you want to step with it, you must also step
        to all the symbols that the key (symbol) belongs to.
        For example:
            a   ab
        q0  q1  q2
        q1  q1  q1
        q2  q2  q2

        If this NFA is in state {q0} and gets the symbol "ab", the
        next state would be {q1, q2}
        """
        symbols = [symbol for symbol in self.alphabet]
        symbols.sort(key=len)
        symbols.reverse()
        for i, symbol in enumerate(symbols):
            for j in range(i+1, len(symbols)):
                if symbol.startswith(symbols[j]) and symbols[j] != "":
                    if symbol in self.nfa_transition_table:
                        self.nfa_transition_table.get(
                            symbol).append(symbols[j])
                    else:
                        self.nfa_transition_table[symbol] = [symbols[j]]

    # todo This e_closure gets called very often if checking if a string is
    # in the language, thus it would be much better to cache the e_closure of
    # all sets
    def calculate_e_closure(self, ids: Iterable[int]) -> Set[State]:
        """Calculates the e closure of some states

        Args:
            ids (Iterable[int]): The ids of the states

        Returns:
            Set[State]: The e closure
        """
        # This could be used, but slows it down a bit
        # super()._check_ids(ids)

        # Just a stack of states that we've already checked
        seen = set()
        # Set of states in e closure
        e_closure = set(self.states[id] for id in ids)

        stack = [id for id in ids]
        while stack:
            _id = stack.pop()
            if _id in seen:
                continue
            seen.add(_id)

            for transition, dests in self.transitions.items():
                # If it has the same origin and it transitions on the empty string
                if transition.origin == _id and transition.string == "":
                    stack.extend([dest.id for dest in dests])
                    e_closure = e_closure | dests

        return e_closure

    def _get_symbols(self, string: str) -> List[List[str]]:
        """Returns the symbols from a string in the right order

        Args:
            string (str): The string to get symbols from

        Returns:
            List[List[str]]: The symbols extracted from the string
        """
        steps = [[step] for step in super()._get_symbols(string)]

        # Get potential additional steps
        # For example if we have a transition on "a", and on "ab",
        # the symbol "ab" will cause a transition on both "a" and "ab"
        for step in steps:
            additional_steps = self.nfa_transition_table.get(step[0])
            if not additional_steps is None:
                step.extend(additional_steps)
        return steps

    def check_string_in_language(self, string: str) -> bool:
        """Check if a string is inside the language of a DFA/NFA

        Args:
            string (str): The string to check

        Returns:
            bool: True if the string is inside the language
        """
        steps = self._get_symbols(string)

        current_states = {self.initial_state}
        new_current_states = set()
        # print(f"========= string is {string} ============")
        # print("steps is", steps)

        # Calculate for all steps
        for symbols in steps:
            # Calculate for each symbol in the symbols
            for symbol in symbols:
                # Get the e closure of the current state
                new_states = self.calculate_e_closure(
                    [state.id for state in current_states])
                for state in new_states:
                    # Get transitions from state "state.id" on symbol "symbol"
                    new_states = self.transitions.get(
                        Transition(state.id, symbol))
                    if not new_states is None:
                        new_current_states = new_current_states | new_states
            current_states = new_current_states
            new_current_states = set()

        current_states = [state for state in self.calculate_e_closure(
            [state.id for state in current_states])]
        return any(state.final for state in current_states)
