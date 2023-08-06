from ftw.upgrade import UpgradeStep
import pkg_resources

IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'


class FixPlone5Profile(UpgradeStep):
    """Fix Plone 5 profile.
    """

    def __call__(self):
        self.setup_install_profile('profile-ftw.upgrade:default')
        if IS_PLONE_5:
            self.install_upgrade_profile()
