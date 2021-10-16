from string import ascii_uppercase
from typing import Any
import collections
import numpy as np
import pprint

alphabet: list[str] = list(ascii_uppercase)


def numb(letter) -> int:
    return alphabet.index(letter)


def alph(number) -> str:
    return alphabet[number]


wheels: dict[str, dict[str, Any]] = {
    "ETW":
        {"wiring_string": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "turnover": []},
    "I":
        {"wiring_string": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "turnover": [numb("Q")]},
    "II":
        {"wiring_string": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "turnover": [numb("E")]},
    "III":
        {"wiring_string": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "turnover": [numb("V")]},
    "IV":
        {"wiring_string": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "turnover": [numb("J")]},
    "V":
        {"wiring_string": "VZBRGITYUPSDNHLXAWMJQOFECK", "turnover": [numb("Z")]},
    "VI":
        {"wiring_string": "JPGVOUMFYQBENHZRDKASXLICTW", "turnover": [numb("M"), numb("Z")]},
    "VII":
        {"wiring_string": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "turnover": [numb("M"), numb("Z")]},
    "VIII":
        {"wiring_string": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "turnover": [numb("M"), numb("Z")]},
    "UKW-A":
        {"wiring_string": "ZYXWVUTSRQPONMLKJIHGFEDCBA", "turnover": []},
    "UKW-B":
        {"wiring_string": "YRUHQSLDPXNGOKMIEBFZCWVJAT", "turnover": []},
    "UKW-C":
        {"wiring_string": "FVPJIAOYEDRZXWGCTKUQSBNMHL", "turnover": []}
}


def wiring_dict(wiring_str: str) -> dict[str, str]:
    d = dict()
    for i, c in enumerate(list(wiring_str)):
        d[alph(i)] = c

    return collections.OrderedDict(sorted(d.items()))


def symmetrical_wiring_dict(wiring_str: str) -> dict[str, str]:
    d = dict()
    for i, c in enumerate(list(wiring_str)):
        if c not in d:
            d[alph(i)] = c
            d[c] = alph(i)
    return d


def random_wiring_string() -> str:
    remaining_alphabet = alphabet[:]

    d = dict()
    for letter in alphabet:
        if letter not in d:
            connection = remaining_alphabet[np.random.randint(0, len(remaining_alphabet))]
            d[letter] = connection
            d[connection] = letter
            remaining_alphabet.remove(letter)
            if letter != connection:
                remaining_alphabet.remove(connection)

    return ''.join(dict(sorted(d.items())).values())


def format_wiring_dict(d) -> str:
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pformat(d)


def validate_wiring(wiring: str) -> None:
    assert len(wiring) == 26, f"Incorrect wiring length. {wiring=}"
