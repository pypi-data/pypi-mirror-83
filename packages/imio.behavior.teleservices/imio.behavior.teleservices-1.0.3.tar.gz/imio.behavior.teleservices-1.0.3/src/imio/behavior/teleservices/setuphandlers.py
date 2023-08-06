# -*- coding: utf-8 -*-

from imio.behavior.teleservices.behaviors.ts_procedure import ITsProcedure
from imio.behavior.teleservices.utils import add_behavior
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "imio.behavior.teleservices:uninstall",
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    add_behavior("Procedure", ITsProcedure.__identifier__)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
