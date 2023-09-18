from typing import Set

from BaseClasses import MultiWorld, CollectionState


def has_item_access_rule(multiworld: MultiWorld, items: Set, entrance: str, player: int):
    if entrance == "UnderWorld":
        multiworld.get_entrance(entrance, player).access_rule = \
            lambda state: has_any_items(state, player, items)
    else:
        multiworld.get_entrance(entrance, player).access_rule = \
            lambda state: has_items(state, player, items)


def has_items(state: CollectionState, player: int, items: Set) -> bool:
    return state.has_all(items, player)


def has_any_items(state: CollectionState, player: int, items: Set) -> bool:
    return state.has_any(items, player)

def set_rules(multiworld: MultiWorld, player: int):
    multiworld.get_entrance("Mist Village", player).access_rule = \
        lambda state: has_items(state, player, {"Bomb Ring"})
    multiworld.get_entrance("Kaipo Inn", player).access_rule = \
        lambda state: has_items(state, player, {"Kaipo Inn Pass"})
    multiworld.get_entrance("Kaipo Bed", player).access_rule = \
        lambda state: has_items(state, player, {"Sand Ruby"})
    multiworld.get_entrance("Baron Castle", player).access_rule = \
        lambda state: has_items(state, player, {"Baron Key"})
    multiworld.get_entrance("Cave Magnes", player).access_rule = \
        lambda state: has_items(state, player, {"Twin Harp"})
    multiworld.get_entrance("Tower of Zot", player).access_rule = \
        lambda state: has_items(state, player, {"Earth Crystal"})
    multiworld.get_entrance("Adamant Grotto", player).access_rule = \
        lambda state: has_items(state, player, {"Hovercraft", "Rat Tail"})
    multiworld.get_entrance("Lower Bab_il", player).access_rule = \
        lambda state: has_items(state, player, {"Dr. Lugae's Key"})
    multiworld.get_entrance("Sealed Cave", player).access_rule = \
        lambda state: has_items(state, player, {"Luca Necklace"})
    multiworld.get_location("Sylph Cave Boss", player).access_rule = \
        lambda state: has_items(state, player, {"Pan"})
    multiworld.get_entrance("UnderWorld", player).access_rule = \
        lambda state: has_any_items(state, player, {"Hovercraft", "Magma Key"})
    multiworld.get_entrance("Moon", player).access_rule = \
        lambda state: has_items(state, player, {"Darkness Crystal"})




