from ftw.upgrade import UpgradeStep


class RemoveUseConsultancyPhaseFeatureSwitch(UpgradeStep):
    """Remove use_consultancy_phase feature switch."""

    def __call__(self):
        self.install_upgrade_profile()
