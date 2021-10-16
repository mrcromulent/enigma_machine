from .utilities import wheels, numb, wiring_dict
from line_profiler_pycharm import profile
import numpy as np


class Rotor:

    name: str
    wiring: dict[str, str]
    rotor_position: int
    notch_positions: list[int]
    ring_setting: int
    forward_mapping: list[int]
    backward_mapping: list[int]

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

        d = {v: k for k, v in self.wiring.items()}
        self.forward_mapping = [numb(i) for i in self.wiring.values()]
        self.backward_mapping = [numb(i) for i in d.keys()]

    @classmethod
    def from_preset(cls, wheel_name: str, rotor_position: int, ring_setting: int) -> 'Rotor':
        assert wheel_name in wheels, f"Unknown wheel {wheel_name=}"

        notch_positions = wheels[wheel_name]["turnover"]
        wiring_str = wheels[wheel_name]["wiring_string"]
        d = wiring_dict(wiring_str)

        return cls(wheel_name, d, rotor_position, notch_positions, ring_setting)

    # @profile
    def encipher_forward(self, k: int) -> int:
        shift = self.rotor_position - self.ring_setting
        return (self.forward_mapping[(k + shift + 26) % 26] - shift + 26) % 26

    # @profile
    def encipher_backward(self, k: int) -> int:
        shift = self.rotor_position - self.ring_setting
        return (self.backward_mapping[(k + shift + 26) % 26] - shift + 26) % 26

    def at_notch(self) -> bool:
        return self.rotor_position in self.notch_positions

    def turnover(self) -> None:
        self.rotor_position = (self.rotor_position + 1) % 26


class RotorTray:

    def __init__(self, rotor_tray: list[Rotor]) -> None:

        self.rotor_tray = rotor_tray
        self.reflector = rotor_tray[0]
        self.left_rotor = rotor_tray[1]
        self.middle_rotor = rotor_tray[2]
        self.right_rotor = rotor_tray[3]

    def rotate(self) -> None:

        if self.middle_rotor.at_notch():
            self.middle_rotor.turnover()
            self.left_rotor.turnover()
        elif self.right_rotor.at_notch():
            self.middle_rotor.turnover()

        self.right_rotor.turnover()

    def forward_pass(self, k: int) -> int:
        k = self.right_rotor.encipher_forward(k)
        k = self.middle_rotor.encipher_forward(k)
        return self.left_rotor.encipher_forward(k)

    def backward_pass(self, k: int) -> int:
        k = self.left_rotor.encipher_backward(k)
        k = self.middle_rotor.encipher_backward(k)
        return self.right_rotor.encipher_backward(k)

    def reflect(self, k: int) -> int:
        return self.reflector.encipher_forward(k)
