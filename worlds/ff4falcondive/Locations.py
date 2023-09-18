from typing import Dict, NamedTuple, Optional

from BaseClasses import Location

class FF4Location(Location):
    game: str = "FF4 Falcon Dive"

class FF4LocationData(NamedTuple):
    group: str
    code: Optional[int] = None

def get_locations_by_group(group: str) -> Dict[str, FF4LocationData]:
    location_data: Dict[str, FF4LocationData] = {}
    for name, data in location_table.items():
        if data.group == group:
            location_data.setdefault(name, data)

    return location_data


id_offset: int = 44445000
location_table: Dict[str, FF4LocationData] = {
    # OverWorld
    "Mist Cave Boss":               FF4LocationData("OverWorld", 1 + id_offset),
    "Damcyan Castle Boss":          FF4LocationData("OverWorld", 2 + id_offset),
    "Waterfall Boss":               FF4LocationData("OverWorld", 3 + id_offset),
    "Antlion Cave Boss":            FF4LocationData("OverWorld", 4 + id_offset),
    "Fabul Defense Boss":           FF4LocationData("OverWorld", 5 + id_offset),
    "Mt. Hobs Boss":                FF4LocationData("OverWorld", 6 + id_offset),
    "Mt. Ordeals Boss":             FF4LocationData("OverWorld", 7 + id_offset),
    "Baron Inn Boss":               FF4LocationData("OverWorld", 8 + id_offset),
    "Mist Village Boss":            FF4LocationData("OverWorld", 9 + id_offset),
    "Kaipo Inn Boss":               FF4LocationData("OverWorld", 10 + id_offset),
    "Kaipo Bed Boss":               FF4LocationData("OverWorld", 11 + id_offset),
    "Baron Castle (King)":          FF4LocationData("OverWorld", 12 + id_offset),
    "Baron Castle (Odin)":          FF4LocationData("OverWorld", 13 + id_offset),
    "Cave Magnes Boss":             FF4LocationData("OverWorld", 14 + id_offset),
    "Tower of Zot Boss":            FF4LocationData("OverWorld", 15 + id_offset),
    "Adamant Grotto":               FF4LocationData("OverWorld", 16 + id_offset),

    # UnderWorld
    "Dwarf Castle Boss":            FF4LocationData("UnderWorld", 17 + id_offset),
    "Lower Bab_il (Top)":           FF4LocationData("UnderWorld", 18 + id_offset),
    "Lower Bab_il (Cannon)":        FF4LocationData("UnderWorld", 19 + id_offset),
    "Sealed Cave Boss":             FF4LocationData("UnderWorld", 20 + id_offset),
    "Feymarch (Queen)":             FF4LocationData("UnderWorld", 21 + id_offset),
    "Feymarch (King)":              FF4LocationData("UnderWorld", 22 + id_offset),
    "Sylph Cave Boss":              FF4LocationData("UnderWorld", 23 + id_offset),

    # Moon
    "Cave Bahamut Boss":            FF4LocationData("Moon", 24 + id_offset),
    "Murasame Altar":               FF4LocationData("Moon", 25 + id_offset),
    "Crystal Sword Altar":          FF4LocationData("Moon", 26 + id_offset),
    "White Spear Altar":            FF4LocationData("Moon", 27 + id_offset),
    "Ribbon Room Boss":             FF4LocationData("Moon", 28 + id_offset),
    "Masamune Altar":               FF4LocationData("Moon", 29 + id_offset),
    "Giant of Bab_il Boss":         FF4LocationData("Moon", 30 + id_offset),

}