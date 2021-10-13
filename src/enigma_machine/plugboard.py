from .utilities import format_wiring_dict


class Plugboard:
    wiring: dict[str, str] = dict()

    def __init__(self, connections: list[tuple[str, str]]) -> None:

        d = dict()
        for end1, end2 in connections:
            assert end1 != end2, f"Cannot plug to itself: {end1=}, {end2=}"
            d[end1] = end2
            d[end2] = end1

        self.wiring = d

    def forward_char(self, c: str) -> str:
        if c in self.wiring:
            return self.wiring[c]
        else:
            return c

    def __str__(self) -> str:
        return format_wiring_dict(self.wiring)
