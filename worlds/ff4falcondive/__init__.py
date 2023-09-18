from .Options import ff4_options
from .Items import item_table, FF4Item, get_items_by_group
from .Locations import location_table, FF4Location
from .Regions import create_regions
# from .Rules import set_rules

from typing import Dict, Any, List
from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld


class FF4WebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the FF4FalconDive integration for Archipelago multi-world games",
        "English",
        "setup_en.md",
        "setup/en",
        ["KindaSneaki"]
    )]


class FF4World(World):
    game: str = "FF4 Falcon Dive"
    option_definitions = ff4_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    data_version = 0
    web = FF4WebWorld()

    def create_items(self) -> None:
        # Generate item pool
        itempool: List = []
        total_locations = len(location_table)
        for item, data in item_table.items():
            quantity = data.max_quantity
            itempool += [self.create_item(item) for _ in range(0, quantity)]

        # Start with 1 character
        self.multiworld.push_precollected(self.multiworld.create_item("Character 1", self.player))

        while len(itempool) < total_locations:
            itempool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += itempool

    def create_item(self, name: str) -> "Item":
        data = item_table[name]
        return FF4Item(name, data.classification, data.code, self.player)

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_group("Filler")
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player)
        # Create Victory event
        create_events(self.multiworld, self.player)

    # def set_rules(self) -> None:
    #     set_rules(self.multiworld, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal": self.multiworld.goal[self.player].value,
            "starting_character": self.multiworld.starting_character[self.player].value,
            "available_characters": self.multiworld.available_characters[self.player].value
        }


def create_events(multiworld: MultiWorld, player: int) -> None:
    victory_region = multiworld.get_region("Zeromus", player)
    victory_event = FF4Location(player, "Victory", None, victory_region)
    victory_event.place_locked_item(FF4Item("Victory", ItemClassification.progression, None, player))
    victory_region.locations.append(victory_event)

    zeromus_region = multiworld.get_region("Zeromus", player)
    shards = multiworld.needed_shards[player].value
    multiworld.get_entrance("Zeromus", player).access_rule = \
        lambda state: state.has("Crystal Shard", player, shards)
    zeromus_event = FF4Location(player, "Defeat Zeromus", None, zeromus_region)
    zeromus_event.place_locked_item(FF4Item("Defeat Zeromus", ItemClassification.progression, None, player))
    zeromus_region.locations.append(zeromus_event)

    # Win Condition
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

