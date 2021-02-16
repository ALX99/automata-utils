from typing import NamedTuple


class Transition(NamedTuple("origin", [("origin", int), ("string", str)])):
    """A Class representing a transition from one state to another

    Args:
        NamedTuple ([type]): The transition
    """
