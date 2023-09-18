from typing import Dict
from Options import Option, OptionSet, Toggle, DefaultOnToggle, DeathLink, Range, Choice


class Goal(Choice):
    """Goal"""
    display_name = "Goal"
    option_zeromous = 0
    option_ordeals = 1


class StartingCharacter(Choice):
    """Starting Character"""
    display_name = "Starting Character"
    option_dark_cecil = 0
    option_paladin_cecil = 1
    option_kain = 2
    option_rosa = 3
    option_rydia = 4
    option_cid = 5
    option_tellah = 6
    option_edward = 7
    option_yang = 8
    option_palom = 9
    option_porom = 10
    option_edge = 11
    option_fusoya = 12


class AvailableCharacters(OptionSet):
    """Available Characters"""
    display_name = "Available Characters"
    default = {"Dark Cecil", "Paladin Cecil", "Kain", "Rosa", "Rydia", "Cid", "Tellah", "Edward", "Yang", "Palom", "Porom", "Edge", "Fusoya"}
    valid_keys = {"Dark Cecil", "Paladin Cecil", "Kain", "Rosa", "Rydia", "Cid", "Tellah", "Edward", "Yang", "Palom", "Porom", "Edge", "Fusoya"}


ff4_options: Dict[str, type(Option)] = {
    "goal":                     Goal,
    "starting_character":       StartingCharacter,
    "available_characters":     AvailableCharacters
}