# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone import api

import cpskin.cirkwi


class CpskinCirkwiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=cpskin.cirkwi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cpskin.cirkwi:default')
        api.user.create(email='test@imio.be', username='test')
        api.user.grant_roles(username='test', roles=['Site Administrator'])

CPSKIN_CIRKWI_FIXTURE = CpskinCirkwiLayer()


CPSKIN_CIRKWI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_CIRKWI_FIXTURE,),
    name='CpskinCirkwiLayer:IntegrationTesting'
)


CPSKIN_CIRKWI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CPSKIN_CIRKWI_FIXTURE,),
    name='CpskinCirkwiLayer:FunctionalTesting'
)


CPSKIN_CIRKWI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CPSKIN_CIRKWI_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CpskinCirkwiLayer:AcceptanceTesting'
)
