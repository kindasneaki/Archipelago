from . import RoR2TestBase

class RoR2ExploreAccessTest(RoR2TestBase):

    def TestGoal(self):
        self.collect_all_but(["Dio's Best Friend"])
        self.assertBeatable(False)
        self.collect_by_name(["Dio's Best Friend"])
        self.assertBeatable(True)
