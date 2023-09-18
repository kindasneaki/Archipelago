from typing import Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification


class FF4Item(Item):
    game: str = "FF4 Falcon Dive"


class FF4ItemData(NamedTuple):
    group: str
    code: Optional[int] = None
    classification = ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1


def get_items_by_group(group: str) -> Dict[str, FF4ItemData]:
    item_dict: Dict[str, FF4ItemData] = {}
    for name, data in item_table.items():
        if data.group == group:
            item_dict.setdefault(name, data)

    return item_dict


id_offset: int = 44444000

item_table: Dict[str, FF4ItemData] = {
    # Characters
    "Character 1":          FF4ItemData("Character", 1 + id_offset, ItemClassification.progression),
    "Character 2":          FF4ItemData("Character", 2 + id_offset, ItemClassification.progression),
    "Character 3":          FF4ItemData("Character", 3 + id_offset, ItemClassification.progression),
    "Character 4":          FF4ItemData("Character", 4 + id_offset, ItemClassification.progression),
    "Character 5":          FF4ItemData("Character", 5 + id_offset, ItemClassification.progression),

    # Key Items
    "Bomb Ring":            FF4ItemData("KeyItem", 71 + id_offset, ItemClassification.progression),
    "Kaipo Inn Pass":       FF4ItemData("KeyItem", 80 + id_offset, ItemClassification.progression),
    "Legend Sword":         FF4ItemData("KeyItem", 131 + id_offset, ItemClassification.progression),
    "Sand Ruby":            FF4ItemData("KeyItem", 64 + id_offset, ItemClassification.progression),
    "Baron Key":            FF4ItemData("KeyItem", 68 + id_offset, ItemClassification.progression),
    "Twin Harp":            FF4ItemData("KeyItem", 69 + id_offset, ItemClassification.progression),
    "Earth Crystal":        FF4ItemData("KeyItem", 66 + id_offset, ItemClassification.progression),
    "Magma Key":            FF4ItemData("KeyItem", 72 + id_offset, ItemClassification.progression),
    "Dr. Lugae's Key":      FF4ItemData("KeyItem", 75 + id_offset, ItemClassification.progression),
    "Hovercraft":           FF4ItemData("KeyItem", 81 + id_offset, ItemClassification.progression),
    "Luca Necklace":        FF4ItemData("KeyItem", 74 + id_offset, ItemClassification.progression),
    "Darkness Crystal":     FF4ItemData("KeyItem", 73 + id_offset, ItemClassification.progression),
    "Rat Tail":             FF4ItemData("KeyItem", 67 + id_offset, ItemClassification.progression),
    "Pink Tail":            FF4ItemData("KeyItem", 70 + id_offset, ItemClassification.useful),
    "Pan":                  FF4ItemData("KeyItem", 62 + id_offset, ItemClassification.progression),
    "Adamant":              FF4ItemData("KeyItem", 63 + id_offset, ItemClassification.progression),
    "Crystal Shard":        FF4ItemData("Crystal", 89 + id_offset, ItemClassification.progression, 4),
}

filler_item_table: Dict[str, FF4ItemData] = {
    # Items
    "Potion":               FF4ItemData("Filler", 200 + id_offset, ItemClassification.filler),
}
