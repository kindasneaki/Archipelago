import string

from .Items import RiskOfRainItem, RiskOfRainItemData, item_table, item_pool_weights, offset, get_items_by_category, \
    filler_table
from .Locations import RiskOfRainLocation, get_classic_item_pickups, item_pickups, orderedstage_location
from .Rules import set_rules
from .RoR2Environments import *

from BaseClasses import Region, Entrance, Item, ItemClassification, MultiWorld, Tutorial
from .Options import ror2_options, ItemWeights
from worlds.AutoWorld import World, WebWorld
from .Regions import create_regions


class RiskOfWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Risk of Rain 2 integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ijwu"]
    )]


class RiskOfRainWorld(World):
    """
     Escape a chaotic alien planet by fighting through hordes of frenzied monsters – with your friends, or on your own.
     Combine loot in surprising ways and master each character until you become the havoc you feared upon your
     first crash landing.
    """
    game: str = "Risk of Rain 2"
    option_definitions = ror2_options
    topology_present = False
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = item_pickups

    data_version = 7
    required_client_version = (0, 4, 3)
    web = RiskOfWeb()
    total_revivals: int

    def generate_early(self) -> None:
        # figure out how many revivals should exist in the pool
        if self.multiworld.goal[self.player] == "classic":
            total_locations = self.multiworld.total_locations[self.player].value
        else:
            total_locations = len(
                orderedstage_location.get_locations(
                    chests=self.multiworld.chests_per_stage[self.player].value,
                    shrines=self.multiworld.shrines_per_stage[self.player].value,
                    scavengers=self.multiworld.scavengers_per_stage[self.player].value,
                    scanners=self.multiworld.scanner_per_stage[self.player].value,
                    altars=self.multiworld.altars_per_stage[self.player].value,
                    dlc_sotv=self.multiworld.dlc_sotv[self.player].value
                )
            )
        self.total_revivals = int(self.multiworld.total_revivals[self.player].value / 100 *
                                  total_locations)
        # self.total_revivals = self.multiworld.total_revivals[self.player].value
        if self.multiworld.start_with_revive[self.player].value:
            self.total_revivals -= 1
        if self.multiworld.victory[self.player] == "voidling" and not self.multiworld.dlc_sotv[self.player]:
            self.multiworld.victory[self.player].value = "any"

    def create_regions(self) -> None:

        if self.multiworld.goal[self.player] == "classic":
            # classic mode
            menu = create_region(self.multiworld, self.player, "Menu")
            self.multiworld.regions.append(menu)
            # By using a victory region, we can define it as being connected to by several regions
            #   which can then determine the availability of the victory.
            victory_region = create_region(self.multiworld, self.player, "Victory")
            self.multiworld.regions.append(victory_region)
            petrichor = create_region(self.multiworld, self.player, "Petrichor V",
                                      get_classic_item_pickups(self.multiworld.total_locations[self.player].value))
            self.multiworld.regions.append(petrichor)

            # classic mode can get to victory from the beginning of the game
            to_victory = Entrance(self.player, "beating game", petrichor)
            petrichor.exits.append(to_victory)
            to_victory.connect(victory_region)

            connection = Entrance(self.player, "Lobby", menu)
            menu.exits.append(connection)
            connection.connect(petrichor)
        else:
            # explore mode
            create_regions(self)

        create_events(self.multiworld, self.player)

    def create_items(self) -> None:
        # shortcut for starting_inventory... The start_with_revive option lets you start with a Dio's Best Friend
        if self.multiworld.start_with_revive[self.player]:
            self.multiworld.push_precollected(self.multiworld.create_item("Dio's Best Friend", self.player))

        environments_pool = {}
        # only mess with the environments if they are set as items
        if self.multiworld.goal[self.player] == "explore":

            # figure out all available ordered stages for each tier
            environment_available_orderedstages_table = environment_vanilla_orderedstages_table
            if self.multiworld.dlc_sotv[self.player]:
                environment_available_orderedstages_table = \
                    collapse_dict_list_vertical(environment_available_orderedstages_table,
                                                environment_sotv_orderedstages_table)

            environments_pool = shift_by_offset(environment_vanilla_table, offset + 700)

            if self.multiworld.dlc_sotv[self.player]:
                environment_offset_table = shift_by_offset(environment_sotv_table, offset + 700)
                environments_pool = {**environments_pool, **environment_offset_table}
            environments_to_precollect = 5 if self.multiworld.begin_with_loop[self.player].value else 1
            # percollect environments for each stage (or just stage 1)
            for i in range(environments_to_precollect):
                unlock = self.multiworld.random.choices(list(environment_available_orderedstages_table[i].keys()), k=1)
                self.multiworld.push_precollected(self.create_item(unlock[0]))
                environments_pool.pop(unlock[0])
        else:
            item_table["Dio's Best Friend"] = RiskOfRainItemData("Upgrade", 1 + offset,
                                                                 ItemClassification.progression_skip_balancing)
            item_table["Dio's Best Friend"] = RiskOfRainItemData("Upgrade", 1 + offset, ItemClassification.progression)

        # Generate item pool
        itempool: List = []
        # Add revive items for the player
        itempool += ["Dio's Best Friend"] * self.total_revivals
        itempool += ["Beads of Fealty"]
        itempool += ["Radar Scanner"]
        itempool += ["Stage 1"]
        itempool += ["Stage 2"]
        itempool += ["Stage 3"]
        itempool += ["Stage 4"]

        for env_name, _ in environments_pool.items():
            itempool += [env_name]

        if self.multiworld.goal[self.player] == "classic":
            # classic mode
            total_locations = self.multiworld.total_locations[self.player].value
        else:
            # explore mode
            total_locations = len(
                orderedstage_location.get_locations(
                    chests=self.multiworld.chests_per_stage[self.player].value,
                    shrines=self.multiworld.shrines_per_stage[self.player].value,
                    scavengers=self.multiworld.scavengers_per_stage[self.player].value,
                    scanners=self.multiworld.scanner_per_stage[self.player].value,
                    altars=self.multiworld.altars_per_stage[self.player].value,
                    dlc_sotv=self.multiworld.dlc_sotv[self.player].value
                )
            )
        # Create junk items
        junk_pool = self.create_junk_pool()
        # Fill remaining items with randomly generated junk
        while len(itempool) < total_locations:
            weights = [data for data in junk_pool.values()]
            filler = self.multiworld.random.choices([filler for filler in junk_pool.keys()], weights,
                                                    k=1)[0]
            itempool.append(filler)

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))
        self.multiworld.itempool += itempool

    def create_junk_pool(self) -> Dict:
        # if presets are enabled generate junk_pool from the selected preset
        pool_option = self.multiworld.item_weights[self.player].value
        junk_pool: Dict[str, int] = {}
        if self.multiworld.item_pool_presets[self.player]:
            # generate chaos weights if the preset is chosen
            if pool_option == ItemWeights.option_chaos:
                for name, max_value in item_pool_weights[pool_option].items():
                    junk_pool[name] = self.multiworld.random.randint(0, max_value)
            else:
                junk_pool = item_pool_weights[pool_option].copy()
        else:  # generate junk pool from user created presets
            junk_pool = {
                "Item Scrap, Green": self.multiworld.green_scrap[self.player].value,
                "Item Scrap, Red": self.multiworld.red_scrap[self.player].value,
                "Item Scrap, Yellow": self.multiworld.yellow_scrap[self.player].value,
                "Item Scrap, White": self.multiworld.white_scrap[self.player].value,
                "Common Item": self.multiworld.common_item[self.player].value,
                "Uncommon Item": self.multiworld.uncommon_item[self.player].value,
                "Legendary Item": self.multiworld.legendary_item[self.player].value,
                "Boss Item": self.multiworld.boss_item[self.player].value,
                "Lunar Item": self.multiworld.lunar_item[self.player].value,
                "Void Item": self.multiworld.void_item[self.player].value,
                "Equipment": self.multiworld.equipment[self.player].value,
                "Money": self.multiworld.money[self.player].value,
                "Lunar Coin": self.multiworld.lunar_coin[self.player].value,
                "1000 Exp": self.multiworld.experience[self.player].value,
                "Mountain Trap": self.multiworld.mountain_trap[self.player].value,
                "Time Warp Trap": self.multiworld.time_warp_trap[self.player].value,
                "Combat Trap": self.multiworld.combat_trap[self.player].value,
                "Teleport Trap": self.multiworld.teleport_trap[self.player].value,
            }
        if not self.multiworld.enable_trap[self.player]:
            junk_pool.pop("Mountain Trap")
            junk_pool.pop("Time Warp Trap")
            junk_pool.pop("Combat Trap")
            junk_pool.pop("Teleport Trap")
        # remove lunar items from the pool
        if not (self.multiworld.enable_lunar[self.player] or pool_option == ItemWeights.option_lunartic):
            junk_pool.pop("Lunar Item")
        # remove void items from the pool
        if not (self.multiworld.dlc_sotv[self.player] or pool_option == ItemWeights.option_void):
            junk_pool.pop("Void Item")

        return junk_pool

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return RiskOfRainItem(name, data.item_type, data.code, self.player)

    def set_rules(self) -> None:
        set_rules(self)

    def get_filler_item_name(self) -> str:
        weights = [data.weight for data in filler_table.values()]
        filler = self.multiworld.random.choices([filler for filler in filler_table.keys()], weights,
                                                k=1)[0]
        return filler

    def fill_slot_data(self):
        return {
            "itemPickupStep": self.multiworld.item_pickup_step[self.player].value,
            "shrineUseStep": self.multiworld.shrine_use_step[self.player].value,
            "goal": self.multiworld.goal[self.player].value,
            "victory": self.multiworld.victory[self.player].value,
            "seed": "".join(self.multiworld.per_slot_randoms[self.player].choice(string.digits) for _ in range(16)),
            "totalLocations": self.multiworld.total_locations[self.player].value,
            "chestsPerStage": self.multiworld.chests_per_stage[self.player].value,
            "shrinesPerStage": self.multiworld.shrines_per_stage[self.player].value,
            "scavengersPerStage": self.multiworld.scavengers_per_stage[self.player].value,
            "scannerPerStage": self.multiworld.scanner_per_stage[self.player].value,
            "altarsPerStage": self.multiworld.altars_per_stage[self.player].value,
            "totalRevivals": self.multiworld.total_revivals[self.player].value,
            "startWithDio": self.multiworld.start_with_revive[self.player].value,
            "finalStageDeath": self.multiworld.final_stage_death[self.player].value,
            "deathLink": self.multiworld.death_link[self.player].value,
            "offset": offset
        }


def create_events(world: MultiWorld, player: int) -> None:
    total_locations = world.total_locations[player].value
    num_of_events = total_locations // 25
    if total_locations / 25 == num_of_events:
        num_of_events -= 1
    world_region = world.get_region("Petrichor V", player)
    if world.goal[player] == "classic":
        # only setup Pickups when using classic_mode
        for i in range(num_of_events):
            event_loc = RiskOfRainLocation(player, f"Pickup{(i + 1) * 25}", None, world_region)
            event_loc.place_locked_item(RiskOfRainItem(f"Pickup{(i + 1) * 25}", ItemClassification.progression, None,
                                                       player))
            event_loc.access_rule = \
                lambda state, i=i: state.can_reach(f"ItemPickup{((i + 1) * 25) - 1}", "Location", player)
            world_region.locations.append(event_loc)
    elif world.goal[player] == "explore":
        event_region = world.get_region("OrderedStage_5", player)
        event_loc = RiskOfRainLocation(player, f"Stage_5", None, event_region)
        event_loc.place_locked_item(RiskOfRainItem(f"Stage 5", ItemClassification.progression, None, player))
        event_loc.show_in_spoiler = False
        event_region.locations.append(event_loc)
        world.get_location(f"Stage_5", player).access_rule = \
            lambda state: state.has("Sky Meadow", player)

    victory_region = world.get_region("Victory", player)
    victory_event = RiskOfRainLocation(player, "Victory", None, victory_region)
    victory_event.place_locked_item(RiskOfRainItem("Victory", ItemClassification.progression, None, player))
    victory_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, locations: Dict[str, int] = {}) -> Region:
    ret = Region(name, player, world)
    for location_name, location_id in locations.items():
        ret.locations.append(RiskOfRainLocation(player, location_name, location_id, ret))
    return ret
