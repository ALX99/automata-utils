from typing import NamedTuple


class State(NamedTuple("state", [("id", int), ("name", str), ("initial", bool), ("final", bool)])):
    pass
