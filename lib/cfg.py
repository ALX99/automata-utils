
import copy
import collections
from typing import Dict, ItemsView, Iterator, List, Set


class Productions:
    def __init__(self) -> None:
        self._productions: Dict[str, List[str]]
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
        return copy.deepcopy(self._productions)

    def get_dict_productions_raw(self) -> Dict[str, List[str]]:
        return self._productions

    def items(self) -> ItemsView[str, List[str]]:
        return self._productions.items()

    def remove_production(self, head: str, tail: str) -> None:
        self._productions[head].remove(tail)
        if len(self._productions[head]) == 0:
            del self._productions[head]

    def remove_unreachable_productions(self, reachable: Set[str] = set()) -> None:
        for _, tails in self._productions.items():
            reachable = reachable.union({char for tail in tails for char in tail})

        reachable = reachable.intersection({head for head in self._productions})
        remove = set()
        for head in self._productions:
            if head not in reachable:
                remove.add(head)
        for head in remove:
            del self._productions[head]

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

    def __eq__(self, o: object) -> bool:
        other_dicts = o.get_dict_productions()
        for head, tails in self._productions.items():
            if collections.Counter(tails) != collections.Counter(other_dicts[head]):
                return False
        return True


class CFG:
    def __init__(self,  start_state: str, productions: Productions = Productions()) -> None:
        self._productions = productions
        self._variables = set()
        self._start_state = start_state

        # Add all variables
        for head in self._productions:
            self._variables.add(head)

    def get_productions(self) -> Productions:
        p = Productions()
        p.set_productions(self._productions.get_dict_productions())
        return p

    def get_start_state(self) -> str:
        return self._start_state

    def get_dict_productions_raw(self) -> Dict[str, List[str]]:
        return self._productions.get_dict_productions_raw()

    def remove_unreachable_productions(self) -> None:
        self._productions.remove_unreachable_productions({self._start_state})

    def get_variables(self) -> Set[str]:
        return self._variables.copy()

    def add_production(self, head: str, tail: str) -> None:
        self._productions.add_production(head, tail)

    def remove_production(self, head: str, tail: str) -> None:
        self._productions.remove_production(head, tail)

    def __repr__(self) -> str:
        return str(self._productions)

    def __eq__(self, o: object) -> bool:
        return self._productions == o.get_productions() and self._start_state == o.get_start_state()
