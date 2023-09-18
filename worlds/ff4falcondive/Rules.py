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
    # Magma Key, Hovercraft, Character 1, Character 2, Character 3
    return state.has_any({"Magma Key", "Hovercraft"}, player) and state.has_all({"Character 1", "Character 2", "Character 3"}, player)
