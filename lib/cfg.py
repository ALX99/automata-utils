
import copy
from typing import Dict, ItemsView, Iterator, List, Set


class Productions:
    def __init__(self) -> None:
        self._productions = dict()

    def add_production(self, head: str, tail: str) -> None:
        # Variables have to have big letters
        for h in head:
            if not h.isupper():
                raise ValueError("Lowercase letter in head")
        if head in self._productions:
            self._productions[head].append(tail)
        else:
            self._productions[head] = [tail]

    def set_productions(self, productions: Dict[str, List[str]]):
        self._productions = productions

    def get_dict_productions(self) -> Dict[str, List[str]]:
        return self._productions.copy()

    def items(self) -> ItemsView[str, List[str]]:
        return self._productions.items()

    def __iter__(self) -> Iterator[str]:
        return self._productions.__iter__()

    def __repr__(self) -> str:
        stringy = ""
        for head, tail in self._productions.items():
            stringy += head+" -> "
            for i, t in enumerate(tail):
                stringy += t+" | "
                if i == len(tail)-1:
                    stringy = stringy[:-3]+"\n"

        return stringy[:-1]


class CFG:
    def __init__(self, productions: Productions = Productions()) -> None:
        self._productions = productions
        self._variables = set()

        # Add all variables
        for head in self._productions:
            self._variables.add(head)

    def get_productions(self) -> Productions:
        p = Productions()
        p.set_productions(self._productions.get_dict_productions())
        return p

    def get_variables(self) -> Set[str]:
        return self._variables.copy()

    def __repr__(self) -> str:
        return str(self._productions)
