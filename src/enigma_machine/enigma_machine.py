from .plugboard import Plugboard
from .utilities import numb, alph
from .rotor import RotorTray


class EnigmaMachine:

    def __init__(self,
                 rotor_tray: RotorTray,
                 plugboard: Plugboard) -> None:

        self.rotor_tray = rotor_tray
        self.plugboard = plugboard

    def encrypt(self, message: str) -> str:
        cipher_text = ""
        for c in list(message.upper()):
            cipher_text += self.encode(c)
        return cipher_text

    def encode(self, c: str) -> str:
        self.rotor_tray.rotate()

        k = numb(self.plugboard.forward_char(c))
        k = self.rotor_tray.forward_pass(k)
        k = self.rotor_tray.reflect(k)
        k = self.rotor_tray.backward_pass(k)
        c_out = self.plugboard.forward_char(alph(k))

        return c_out


def main():
    pass


if __name__ == "__main__":
    main()
