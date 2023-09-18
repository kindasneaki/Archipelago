from typing import Dict, List, NamedTuple, Optional, Set

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import FF4Location, location_table
from .Rules import has_item_access_rule


class FF4RegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]
    required_item: Optional[Set[str]] = None


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, FF4RegionData] = {
        # OverWorld
        "Menu":                 FF4RegionData(None, ["OverWorld"]),
        "OverWorld":            FF4RegionData(None, ["Mist Cave", "Damcyan Castle", "Waterfall", "Antlion Cave",
                                                     "Fabul Defense", "Mt. Hobs", "Mt. Ordeals", "Baron Inn",
                                                     "Mist Village", "Kaipo Inn", "Kaipo Bed", "Baron Castle",
                                                     "Cave Magnes", "Tower of Zot",
                                                     "Adamant Grotto", "UnderWorld"]),
        "Mist Cave":            FF4RegionData(["Mist Cave Boss"], []),
        "Damcyan Castle":       FF4RegionData(["Damcyan Castle Boss"], []),
        "Waterfall":            FF4RegionData(["Waterfall Boss"], []),
        "Antlion Cave":         FF4RegionData(["Antlion Cave Boss"], []),
        "Fabul Defense":        FF4RegionData(["Fabul Defense Boss"], []),
        "Mt. Hobs":             FF4RegionData(["Mt. Hobs Boss"], []),
        "Mt. Ordeals":          FF4RegionData(["Mt. Ordeals Boss"], [], {"Character 2"}),
        "Baron Inn":            FF4RegionData(["Baron Inn Boss"], [], {"Character 2"}),
        "Mist Village":         FF4RegionData(["Mist Village Boss"], [], {"Bomb Ring"}),
        "Kaipo Inn":            FF4RegionData(["Kaipo Inn Boss"], [], {"Kaipo Inn Pass"}),
        "Kaipo Bed":            FF4RegionData(["Kaipo Bed Boss"], [], {"Sand Ruby"}),
        "Baron Castle":         FF4RegionData(["Baron Castle (King)", "Baron Castle (Odin)"], [],
                                              {"Baron Key", "Character 2", "Character 3"}),
        "Cave Magnes":          FF4RegionData(["Cave Magnes Boss"], [], {"Twin Harp", "Character 2"}),
        "Tower of Zot":         FF4RegionData(["Tower of Zot Boss"], [], {"Earth Crystal", "Character 2"}),
        "Adamant Grotto":       FF4RegionData(["Adamant Grotto"], [], {"Hovercraft", "Rat Tail"}),

        # UnderWorld
        "UnderWorld":           FF4RegionData(None,
                                              ["Dwarf Castle", "Lower Bab_il", "Sealed Cave", "Feymarch", "Sylph Cave",
                                               "Moon"],
                                              {"Magma Key", "Hovercraft", "Character 1", "Character 2", "Character 3"}),
        "Dwarf Castle":         FF4RegionData(["Dwarf Castle Boss"], []),
        "Lower Bab_il":         FF4RegionData(["Lower Bab_il (Top)", "Lower Bab_il (Cannon)"], [], {"Dr. Lugae's Key"}),
        "Sealed Cave":          FF4RegionData(["Sealed Cave Boss"], [], {"Luca Necklace"}),
        "Feymarch":             FF4RegionData(["Feymarch (Queen)", "Feymarch (King)"], []),
        "Sylph Cave":           FF4RegionData(["Sylph Cave Boss"], [], {"Pan"}),

        # Moon
        "Moon":                 FF4RegionData(None, ["Cave Bahamut", "Lunar Subterrane", "Giant of Bab_il", "Zeromus"],
                                              {"Darkness Crystal", "Character 2", "Character 3", "Character 4"}),
        "Cave Bahamut":         FF4RegionData(["Cave Bahamut Boss"], []),
        "Lunar Subterrane":     FF4RegionData(["Murasame Altar", "Crystal Sword Altar", "White Spear Altar",
                                               "Ribbon Room Boss", "Masamune Altar"], []),
        "Giant of Bab_il":      FF4RegionData(["Giant of Bab_il Boss"], []),
        "Zeromus":              FF4RegionData([], ["Victory"]),
        "Victory":              FF4RegionData(None, [], {"Defeat Zeromus"})
    }
    # Create all the regions
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))

    if not multiworld.moon_after_underground[player]:
        regions["UnderWorld"].region_exits.remove("Moon")
        regions["OverWorld"].region_exits.append("Moon")
    # Connect all the regions to their exits
    for name, data in regions.items():
        create_connections_in_regions(multiworld, player, name, data)


def create_region(multiworld: MultiWorld, player: int, name: str, data: FF4RegionData) -> Region:
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = FF4Location(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)
    return region


def create_connections_in_regions(multiworld: MultiWorld, player: int, name: str, data: FF4RegionData):
    region = multiworld.get_region(name, player)
    if data.region_exits:
        for region_exit in data. region_exits:
            r_exit_stage = Entrance(player, region_exit, region)
            exit_region = multiworld.get_region(region_exit, player)
            r_exit_stage.connect(exit_region)
            region.exits.append(r_exit_stage)

    if data.required_item:
        has_item_access_rule(multiworld, data.required_item, name, player)
