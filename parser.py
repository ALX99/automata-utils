import xml.etree.ElementTree as ET
from typing import Dict, List

from automaton import Automaton
from nfa import NFA
from state import State
from transition import Transition


def parse_states(root: ET.Element) -> List[State]:
    """Parses the JFLAP xml to get a dict of states

    Args:
        root (ET.Element): The root of the JFLAP xml document

    Returns:
        Dict[State]: A dict of all states
    """
    _states = []

    # Parse id, name, initial, and final
    for state in root.findall("automaton")[0].findall("state"):
        name = str(state.get("name"))
        identifier = int(str(state.get("id")))
        initial = len(state.findall("initial")) > 0
        final = len(state.findall("final")) > 0

        _states.append(State(id=identifier, name=name,
                             initial=initial, final=final))

    return _states


def parse_transitions(root: ET.Element) -> Dict[Transition, List[int]]:
    """Parses the JFLAP xml to get a dict of transitions

    Args:
        root (ET.Element): The root of the JFLAP xml document

    Returns:
        Dict[Transition, List[int]]: The dict of transitions
    """
    transitions_ = dict()

    for trans in root.findall("automaton")[0].findall("transition"):
        orig = trans.find("from").text
        dests = trans.find("to").text
        string = trans.find("read").text

        if orig is None or dests is None:
            print("Wtf")
            exit(1)
        if string is None:
            string = ""

        k = Transition(int(orig), str(string))
        if k in transitions_:
            transitions_[k].append(int(dests))
        else:
            transitions_[k] = [int(dests)]

    return transitions_


def parse_jflap_xml(path: str) -> Automaton:
    root = ET.parse(path).getroot()
    states = parse_states(root)
    transitions = parse_transitions(root)
    # todo check if it is an dfa or nfa
    return NFA(states, transitions)
