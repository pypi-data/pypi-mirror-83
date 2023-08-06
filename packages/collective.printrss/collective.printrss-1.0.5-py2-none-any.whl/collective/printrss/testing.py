# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from plone import api

import collective.printrss


class CollectivePrintrssLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.printrss)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.printrss:default')
        api.user.create(email='test@imio.be', username='test')
        api.user.grant_roles(username='test', roles=['Site Administrator'])

COLLECTIVE_PRINTRSS_FIXTURE = CollectivePrintrssLayer()


COLLECTIVE_PRINTRSS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PRINTRSS_FIXTURE,),
    name='CollectivePrintrssLayer:IntegrationTesting'
)


COLLECTIVE_PRINTRSS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PRINTRSS_FIXTURE,),
    name='CollectivePrintrssLayer:FunctionalTesting'
)


COLLECTIVE_PRINTRSS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PRINTRSS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectivePrintrssLayer:AcceptanceTesting'
)
