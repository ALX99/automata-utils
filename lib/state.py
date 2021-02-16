from typing import NamedTuple


class State(NamedTuple("state", [("id", int), ("name", str), ("initial", bool), ("final", bool)])):
    pass


def combine_states(s1: State, s2: State, is_final: bool) -> State:
    """Combines two state

    Args:
        s1 (State): [description]
        s2 (State): [description]
        is_final (bool): [description]

    Returns:
        State: [description]
    """
    return State(int(str(s1.id)+str(s2.id)), s1.name+"_" +
                 s2.name, s1.initial or s1.initial, is_final)
