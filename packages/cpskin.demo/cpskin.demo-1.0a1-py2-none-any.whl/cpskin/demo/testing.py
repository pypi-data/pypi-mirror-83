# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cpskin.demo


class CpskinDemoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=cpskin.demo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.demo:default')


CPSKIN_DEMO_FIXTURE = CpskinDemoLayer()


CPSKIN_DEMO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_DEMO_FIXTURE,),
    name='CpskinDemoLayer:IntegrationTesting'
)


CPSKIN_DEMO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_DEMO_FIXTURE,),
    name='CpskinDemoLayer:FunctionalTesting'
)


CPSKIN_DEMO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CPSKIN_DEMO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CpskinDemoLayer:AcceptanceTesting'
)
