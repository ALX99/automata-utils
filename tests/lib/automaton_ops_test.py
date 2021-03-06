

from lib.automaton_ops import dell, bin, unit
from lib.parser import parse_cfg_string


def test_del():
    cfg = parse_cfg_string('''S -> ABAC
A -> aA | !
B -> bB | !
C -> c''')
    expected = parse_cfg_string('''S -> ABAC | AAC | BAC | AC | ABC | BC | C 
A -> aA | a
B -> bB | b
C -> c''')
    res = dell(cfg, False)
    assert res == expected and res != cfg


def test_bin():
    cfg = parse_cfg_string('''E -> EOE | N
O -> + | - | !
N -> 1 | 1N''')
    expected = parse_cfg_string('''E -> EA | N
A -> OE
O -> + | - | !
N -> 1 | 1N''')
    res = bin(cfg, False)
    assert res == expected and res != cfg


def test_unit():
    cfg = parse_cfg_string('''S -> XY
X -> a
Y -> Z | b
Z -> M
M -> N
N -> a''')
    expected = parse_cfg_string('''S -> XY
X -> a
Y -> a | b ''')
    res = unit(cfg, False)
    res.remove_unreachable_productions()
    assert res == expected and res != cfg
