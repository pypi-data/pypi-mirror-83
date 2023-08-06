# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cpskin.localfood


class CpskinLocalfoodLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=cpskin.localfood)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.localfood:default')


CPSKIN_LOCALFOOD_FIXTURE = CpskinLocalfoodLayer()


CPSKIN_LOCALFOOD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_LOCALFOOD_FIXTURE,),
    name='CpskinLocalfoodLayer:IntegrationTesting'
)


CPSKIN_LOCALFOOD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_LOCALFOOD_FIXTURE,),
    name='CpskinLocalfoodLayer:FunctionalTesting'
)


CPSKIN_LOCALFOOD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CPSKIN_LOCALFOOD_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CpskinLocalfoodLayer:AcceptanceTesting'
)
