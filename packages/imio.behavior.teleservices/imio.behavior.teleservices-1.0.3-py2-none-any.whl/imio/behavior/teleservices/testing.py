# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import imio.behavior.teleservices


class ImioBehaviorTeleservicesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.behavior.teleservices)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'imio.behavior.teleservices:default')


IMIO_BEHAVIOR_TELESERVICES_FIXTURE = ImioBehaviorTeleservicesLayer()


IMIO_BEHAVIOR_TELESERVICES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_BEHAVIOR_TELESERVICES_FIXTURE,),
    name='ImioBehaviorTeleservicesLayer:IntegrationTesting',
)


IMIO_BEHAVIOR_TELESERVICES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_BEHAVIOR_TELESERVICES_FIXTURE,),
    name='ImioBehaviorTeleservicesLayer:FunctionalTesting',
)


IMIO_BEHAVIOR_TELESERVICES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIO_BEHAVIOR_TELESERVICES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='ImioBehaviorTeleservicesLayer:AcceptanceTesting',
)
