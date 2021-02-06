import re
from parser import parse_jflap_xml

from automaton_ops import verify_against_method, verify_against_regex

if __name__ == "__main__":
    automaton = parse_jflap_xml("")

    def tmp(s):
        regex = re.compile(r"^.*baa.*$")
        if regex.match(s):
            return True

        l = len(s)
        for i in range(l-2):
            if s[i] == "a":
                if s[i+1] != "b" or s[i+2] != "b":
                    return False
                i += 2
        return s[l-1] != "a" and s[l-2] != "a"
    # print(verify_against_regex(
    #     automaton, re.compile(r"^((?!bba).)*$"), max_sample_num=20))
    print(verify_against_method(
        automaton, tmp, max_sample_num=10))
    # print(automaton.check_string_in_language("ba"))


# Don't match strings containing bba
# re.compile(r"^((?!bba).)*$")

# Match word baa
# re.compile(r"^.*baa.*$")

# Match an even number of a's
# re.compile(r"^[^a]*(a[^a]*a[^a]*)*$")
