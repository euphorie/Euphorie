from ftw.upgrade import UpgradeStep


class AddUseConsultancyPhaseFeatureSwitch(UpgradeStep):
    """Add use_consultancy_phase feature switch."""

    def __call__(self):
        self.install_upgrade_profile()
