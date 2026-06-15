from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RegionData:
    name: str
    connections: List[str]


region_list: List[RegionData] = [
    RegionData("Menu", ["Main Island"]),
    RegionData("Main Island", ["Floating Islands", "Paradise Island"]),
    RegionData("Floating Islands", []),
    RegionData("Paradise Island", ["Courtroom"]),
    RegionData("Courtroom", ["Trial: Menu"]),
    RegionData("Trial: Menu", ["Trial: Henry's Escape"]),
    RegionData("Trial: Henry's Escape", ["Trial: Henry's Possession"]),
    RegionData("Trial: Henry's Possession", ["Trial: Grace Bloodlines"]),
    RegionData("Trial: Grace Bloodlines", ["Trial: Crimson Agenda"]),
    RegionData("Trial: Crimson Agenda", ["Trial: Doom Jazz Partnership"]),
    RegionData("Trial: Doom Jazz Partnership", ["Trial: Yuri Testimony"]),
    RegionData("Trial: Yuri Testimony", ["Trial: Lydia & Sam Accusation"]),
    RegionData("Trial: Lydia & Sam Accusation", ["Trial: Carmelina Betrayal"]),
    RegionData("Trial: Carmelina Betrayal", ["Trial: Witness Corroboration"]),
    RegionData("Trial: Witness Corroboration", ["Trial: Final Argument"]),
    RegionData("Trial: Final Argument", ["Trial: Conviction"]),
    RegionData("Trial: Conviction", []),
]

region_dictionary: Dict[str, RegionData] = {
    region.name: region
    for region in region_list
}
