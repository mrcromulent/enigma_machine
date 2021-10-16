from enigma_machine.enigma_machine import EnigmaMachine
from enigma_machine.rotor import RotorTray, Rotor
from enigma_machine.plugboard import Plugboard


def test_encode_1():
    rt = RotorTray(
        [
            Rotor.from_preset("UKW-B", 0, 0),
            Rotor.from_preset("I", 0, 0),
            Rotor.from_preset("II", 0, 0),
            Rotor.from_preset("III", 0, 0),
        ])
    pb = Plugboard([])
    e = EnigmaMachine(rt, pb)
    inp = "ABCDEFGHIJKLMNOPQRSTUVWXYZAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = "BJELRQZVJWARXSNBXORSTNCFMEYHCXTGYJFLINHNXSHIUNTHEORXOPLOVFEKAGADSPNPCMHRVZCYECDAZIHVYGPITMSRZKGGHLSRBLHL"
    cipher_text = e.encrypt(inp)
    assert cipher_text == out, f"Incorrect ciphertext. {cipher_text=}"


def test_encode_2():
    rt = RotorTray(
        [
            Rotor.from_preset("UKW-B", 0, 0),
            Rotor.from_preset("VII", 10, 1),
            Rotor.from_preset("V", 5, 2),
            Rotor.from_preset("IV", 12, 3),
        ])
    pb = Plugboard([])
    e = EnigmaMachine(rt, pb)
    inp = "ABCDEFGHIJKLMNOPQRSTUVWXYZAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBABCDEFGHIJKLMNOPQRSTUVWXYZ"
    out = "FOTYBPKLBZQSGZBOPUFYPFUSETWKNQQHVNHLKJZZZKHUBEJLGVUNIOYSDTEZJQHHAOYYZSENTGXNJCHEDFHQUCGCGJBURNSEDZSEPLQP"
    cipher_text = e.encrypt(inp)
    assert cipher_text == out, f"Incorrect ciphertext. {cipher_text=}"


def test_plugboard():
    rt = RotorTray(
        [
            Rotor.from_preset("UKW-B", 0, 0),
            Rotor.from_preset("I", 0, 0),
            Rotor.from_preset("II", 0, 0),
            Rotor.from_preset("III", 0, 0),
        ])
    pb = Plugboard([('A', 'C'), ('F', 'G'), ('J', 'Y'), ('L', 'W')])
    e = EnigmaMachine(rt, pb)
    inp = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    out = "QREBNMCYZELKQOJCGJVIVGLYEMUPCURPVPUMDIWXPPWROOQEGI"
    cipher_text = e.encrypt(inp)
    assert cipher_text == out, f"Incorrect ciphertext. {cipher_text=}"


def test_decode():
    rt = RotorTray(
        [
            Rotor.from_preset("UKW-B", 0, 0),
            Rotor.from_preset("II", 7, 12),
            Rotor.from_preset("V", 4, 2),
            Rotor.from_preset("III", 19, 20),
        ])
    pb = Plugboard([('A', 'F'), ('T', 'V'), ('K', 'O'), ('B', 'L'), ('R', 'W')])
    e = EnigmaMachine(rt, pb)
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
    decoded_text = e.encrypt(inp)
    assert decoded_text == exp, f"Incorrect decoded text. {decoded_text=}"
