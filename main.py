from enigma_machine.enigma_machine import EnigmaMachine
from enigma_machine.rotor import Rotor, RotorTray
from enigma_machine.plugboard import Plugboard
from enigma_machine.utilities import alph, numb, alphabet
from line_profiler_pycharm import profile
import itertools
import numpy as np
from tqdm import tqdm


# @profile
def compute_ioc(text: str) -> float:

    c = len(alphabet)
    n = len(text)
    numerator = 0.0
    for letter in alphabet:
        count = text.count(letter)
        numerator += count * (count - 1)
    denominator = (n * (n - 1) / c)

    return numerator / denominator


def main():
    inp = "OZLUDYAKMGMXVFVARPMJIKVWPMBVWMOIDHYPLAYUWGBZFAFAFUQFZQISLEZMYPVBRDDLAGIHIFUJDFADORQOOMIZPYXDCBPWDSSNUSYZT" \
          "JEWZPWFBWBMIEQXRFASZLOPPZRJKJSPPSTXKPUWYSKNMZZLHJDXJMMMDFODIHUBVCXMNICNYQBNQODFQLOGPZYXRJMTLMRKQAUQJPADHD" \
          "ZPFIKTQBFXAYMVSZPKXIQLOQCVRPKOBZSXIUBAAJBRSNAFDMLLBVSYXISFXQZKQJRIQHOSHVYJXIFUZRMXWJVWHCCYHCXYGRKMKBPWRDB" \
          "XXRGABQBZRJDVHFPJZUSEBHWAEOGEUQFZEEBDCWNDHIAQDMHKPRVYHQGRDYQIOEOLUBGBSNXWPZCHLDZQBWBEWOCQDBAFGUVHNGCIKXEI" \
          "ZGIZHPJFCTMNNNAUXEVWTWACHOLOLSLTMDRZJZEVKKSSGUUTHVXXODSKTFGRUEIIXVWQYUIPIDBFPGLBYXZTCOQBCAHJYNSGDYLREYBRA" \
          "KXGKQKWJEKWGAPTHGOMXJDSQKYHMFGOLXBSKVLGNZOAXGVTGXUIVFTGKPJU"

    exp = "IPROPOSETOCONSIDERTHEQUESTIONCANMACHINESTHINKTHISSHOULDBEGINWITHDEFINITIONSOFTHEMEANINGOFTHETERMSMACHINEA" \
          "NDTHINKTHEDEFINITIONSMIGHTBEFRAMEDSOASTOREFLECTSOFARASPOSSIBLETHENORMALUSEOFTHEWORDSBUTTHISATTITUDEISDANG" \
          "EROUSIFTHEMEANINGOFTHEWORDSMACHINEANDTHINKARETOBEFOUNDBYEXAMININGHOWTHEYARECOMMONLYUSEDITISDIFFICULTTOESC" \
          "APETHECONCLUSIONTHATTHEMEANINGANDTHEANSWERTOTHEQUESTIONCANMACHINESTHINKISTOBESOUGHTINASTATISTICALSURVEYSU" \
          "CHASAGALLUPPOLLBUTTHISISABSURDINSTEADOFATTEMPTINGSUCHADEFINITIONISHALLREPLACETHEQUESTIONBYANOTHERWHICHISC" \
          "LOSELYRELATEDTOITANDISEXPRESSEDINRELATIVELYUNAMBIGUOUSWORDS"

    # print(compute_ioc(inp))
    # print(compute_ioc(exp))
    #
    expected_english_ioc = 1.73
    # expected_german_ioc = 2.05

    # Find rotors
    available_rotors = ["I", "II", "III", "IV", "V"]
    pb = Plugboard([])

    ioc_scores = []
    combinations = []
    ring_positions = []
    explore_range = 26

    for rotors in list(itertools.permutations(available_rotors, 3)):
        print(f"Combination: {rotors=}")

        top_ioc = - np.inf
        top_positions = ()
        for rp1, rp2, rp3 in list(itertools.product(range(explore_range), repeat=3)):
            rt = RotorTray([
                Rotor.from_preset("UKW-B", 0, 0),
                Rotor.from_preset(rotors[0], rp1, 0),
                Rotor.from_preset(rotors[1], rp2, 0),
                Rotor.from_preset(rotors[2], rp3, 0)
            ])
            e = EnigmaMachine(rt, pb)
            decoded_text = e.encrypt(inp)
            ioc = compute_ioc(decoded_text)

            if ioc > top_ioc:
                top_ioc = ioc
                top_positions = (rp1, rp2, rp3)

        ioc_scores.append(top_ioc)
        combinations.append(rotors)
        ring_positions.append(top_positions)

    # Expected answer: II, V, III
    print(sorted(zip(ioc_scores, combinations)))


if __name__ == '__main__':
    main()
