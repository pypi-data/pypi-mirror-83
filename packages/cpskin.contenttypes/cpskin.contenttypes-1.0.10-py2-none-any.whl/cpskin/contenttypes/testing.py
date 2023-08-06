# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cpskin.contenttypes


class CpskinContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=cpskin.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.contenttypes:default')


CPSKIN_CONTENTTYPES_FIXTURE = CpskinContenttypesLayer()


CPSKIN_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_CONTENTTYPES_FIXTURE,),
    name='CpskinContenttypesLayer:IntegrationTesting',
)


CPSKIN_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_CONTENTTYPES_FIXTURE,),
    name='CpskinContenttypesLayer:FunctionalTesting',
)


CPSKIN_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CPSKIN_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CpskinContenttypesLayer:AcceptanceTesting',
)
