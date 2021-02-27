"""This module contains logic to parsing stuff"""
import xml.etree.ElementTree as ET
from typing import Dict, List, Set, Tuple

from lib.cfg import CFG, Productions
from lib.dfa import DFA
from lib.nfa import NFA
from lib.state import State
from lib.transition import Transition


def parse_states(root: ET.Element) -> Set[State]:
    """Parses the JFLAP xml to get a dict of states

    Args:
        root (ET.Element): The root of the JFLAP xml document

    Returns:
        Dict[State]: A dict of all states
    """
    states = set()

    # Parse id, name, initial, and final
    for state in root.findall("automaton")[0].findall("state"):
        name = str(state.get("name"))
        identifier = int(str(state.get("id")))
        initial = len(state.findall("initial")) > 0
        final = len(state.findall("final")) > 0

        states.add(State(id=identifier, name=name,
                         initial=initial, final=final))

    return states


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


def parse_jflap_xml(path: str) -> Tuple[Set[State],
                                        Dict[Transition, List[int]]]:
    """Parses a JFLAP xml file to return a set of states and transitions

    Args:
        path (str): The path to the JFLAP xml file

    Returns:
        Tuple[Set[State], Dict[Transition, List[int]]]: Tuple of states and transitions
    """
    root = ET.parse(path).getroot()
    return (parse_states(root), parse_transitions(root))


def parse_jflap_dfa(path: str) -> DFA:
    """Parses a JFLAP xml file and returns a DFA

    Args:
        path (str): The path to the JFLAP xml file

    Returns:
        DFA: The DFA
    """
    states, transitions = parse_jflap_xml(path)
    return DFA(states, transitions)


def parse_jflap_nfa(path: str) -> NFA:
    """Parses a JFLAP xml file and returns a NFA

    Args:
        path (str): The path to the JFLAP xml file

    Returns:
        NFA: The NFA
    """
    states, transitions = parse_jflap_xml(path)
    return NFA(states, transitions)


def parse_cfg(path: str) -> CFG:
    with open(path) as f:
        lines = f.read().splitlines()

    # Can not contain productions like
    # A -> b
    # A -> c
    # It has to be in the form
    # A -> b | c
    productions = Productions()
    for line in lines:
        l1 = line.split("->")
        for l in l1[1].split("|"):
            productions.add_production(l1[0].strip(), l.strip())

    return CFG(productions)
