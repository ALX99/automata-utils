"""Module containing the DFA class"""

from lib.automaton import Automaton


class DFA(Automaton):
    """Class represeting an NFA"""

    def check_string_in_language(self, string: str) -> bool:
        """Check if a string is inside the language this DFA

        Args:
            string (str): The string to check

        Returns:
            bool: True if the string is inside the language
        """
        steps = super()._get_symbols(string)
        current_state = self.initial_state

        # Calculate for all steps
        for step in steps:
            # Get transitions from state "state.id" and symbol "symbol"
            current_state = super().get_transition(current_state.id, step)
            # DFA has died here
            if current_state is None or len(current_state) == 0:
                return False
            # This is ok since a DFA should only contain transition
            # to at most one other state
            current_state = current_state.copy().pop()

        return current_state.final
