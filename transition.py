from collections import namedtuple
from typing import NamedTuple


class Transition(NamedTuple("origin", [("origin", int), ("string", str)])):
    pass
