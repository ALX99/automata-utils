"""Module containing the DFA class"""

from typing import Optional

from lib.automaton import Automaton
from lib.state import State
from lib.transition import Transition


class DFA(Automaton):
    """Class represeting an NFA"""

    def get_transition(self, state_id: int, symbol: str) -> Optional[State]:
        state = super().get_transition(state_id, symbol)
        if state is None:
            return None
        return state.copy().pop()

    def check_string_in_language(self, string: str) -> bool:
        """Check if a string is inside the language this DFA

        Args:
            string (str): The string to check

        Returns:
            bool: True if the string is inside the language
        """
        symbols = super()._get_symbols(string)
        current_state = self.initial_state

        # Calculate for all steps
        for symbol in symbols:
            current_state = self.get_transition(current_state.id, symbol)
            if current_state is None:
                return False

        return current_state.final

    def check_complete(self) -> bool:
        """Check that the DFA does not have missing transitions

        Returns:
            bool: True if the DFA has no missing transitions
        """
        for state in self.states:
            for symbol in self.alphabet:
                if self.get_transition(state, symbol) is None:
                    return False

        return True
