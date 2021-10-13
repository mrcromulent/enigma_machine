from .utilities import wheels, numb, wiring_dict
import numpy as np


class Rotor:

    def __init__(self,
                 name: str,
                 wiring: dict[str, str],
                 rotor_position: int,
                 notch_positions: list[int],
                 ring_setting: int) -> None:

        self.name = name
        self.wiring = wiring
        self.rotor_position = rotor_position
        self.notch_positions = notch_positions
        self.ring_setting = ring_setting

    @classmethod
    def from_preset(cls, wheel_name: str, rotor_position: int, ring_setting: int) -> 'Rotor':
        assert wheel_name in wheels, f"Unknown wheel {wheel_name=}"

        notch_positions = wheels[wheel_name]["turnover"]
        wiring_str = wheels[wheel_name]["wiring_string"]
        d = wiring_dict(wiring_str)

        return cls(wheel_name, d, rotor_position, notch_positions, ring_setting)

    def encipher(self, k: int, direction='Forward'):
        shift = self.rotor_position - self.ring_setting

        if direction == 'Forward':
            d = self.wiring
            mapping = [numb(i) for i in d.values()]
        else:
            d = {v: k for k, v in self.wiring.items()}
            mapping = np.empty(26, dtype=int)
            for i, c in enumerate(d):
                mapping[numb(c)] = int(i)
            mapping = list(mapping)

        return (mapping[(k + shift + 26) % 26] - shift + 26) % 26

    def at_notch(self):
        return self.rotor_position in self.notch_positions

    def turnover(self):
        self.rotor_position = (self.rotor_position + 1) % 26


class RotorTray:

    def __init__(self, rotor_tray: list[Rotor]):

        self.rotor_tray = rotor_tray
        self.reflector = rotor_tray[0]
        self.left_rotor = rotor_tray[1]
        self.middle_rotor = rotor_tray[2]
        self.right_rotor = rotor_tray[3]

    def rotate(self):

        if self.middle_rotor.at_notch():
            self.middle_rotor.turnover()
            self.left_rotor.turnover()
        elif self.right_rotor.at_notch():
            self.middle_rotor.turnover()

        self.right_rotor.turnover()

    def forward_pass(self, k: int):
        k = self.right_rotor.encipher(k, direction='Forward')
        k = self.middle_rotor.encipher(k, direction='Forward')
        return self.left_rotor.encipher(k, direction='Forward')

    def backward_pass(self, k: int):
        k = self.left_rotor.encipher(k, direction='Backward')
        k = self.middle_rotor.encipher(k, direction='Backward')
        return self.right_rotor.encipher(k, direction='Backward')

    def reflect(self, k: int):
        return self.reflector.encipher(k, direction='Forward')


if __name__ == '__main__':
    r = Rotor.from_preset("III", 0, 0)
    print([numb(i) for i in r.wiring.values()])
