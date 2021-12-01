from ftw.upgrade import UpgradeStep


class AddLeadImageBehaviorToSurvey(UpgradeStep):
    """Add lead image behavior to survey."""

    def __call__(self):
        self.install_upgrade_profile()
