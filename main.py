import re
from parser import parse_jflap_dfa, parse_jflap_nfa

from automaton_ops import verify_against_method, verify_against_regex

if __name__ == "__main__":
    automaton = parse_jflap_dfa("/mnt/c/Users/Alex/Desktop/tmp.jff")

    def tmp(s):
        return "00" not in s and len(s) >= 2 and s[0] == "1" and s[-1] == "1"
    verify_against_method(
        automaton, tmp, max_sample_num=40)


# Don't match strings containing bba
# re.compile(r"^((?!bba).)*$")

# Match word baa
# re.compile(r"^.*baa.*$")

# Match an even number of a's
# re.compile(r"^[^a]*(a[^a]*a[^a]*)*$")
