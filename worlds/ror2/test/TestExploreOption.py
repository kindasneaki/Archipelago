from . import RoR2TestBase

from BaseClasses import CollectionState
from worlds.AutoWorld import AutoWorldRegister


class RoR2ExploreAccessTest(RoR2TestBase):
    options = {
        "goal": 1
    }

    def testLocations(self):
        for location in self.multiworld.get_locations(self):
            self.can_reach_location(location)

    def testEntrance(self):
        for entrance in self.multiworld.get_entrances():
            self.can_reach_entrance(entrance)

    def testGoal(self):
        self.collect_by_name(["Distant Roost", "Distant Roost (2)", "Titanic Plains", "Titanic Plains (2)", "Stage_1"])
        self.assertBeatable(False)
        self.collect_by_name(["Abandoned Aqueduct", "Wetlands Aspect", "Stage_2"])
        self.assertBeatable(False)
        self.collect_by_name(["Rallypoint Delta", "Scorched Acres", "Stage_3"])
        self.assertBeatable(False)
        self.collect_by_name(["Abyssal Depths", "Siren's Call", "Sundered Grove", "Stage_4"])
        self.assertBeatable(False)
        self.collect_by_name(["Sky Meadow", "Stage_5"])
        self.assertBeatable(False)
        self.collect_by_name(["Commencement"])
        self.assertBeatable(True)





