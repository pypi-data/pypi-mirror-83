# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
import imio.pm.ws
from Products.PloneMeeting.testing import PMLayer


class WSCLIENTLayer(PMLayer):
    """ """


WS4PMCLIENT_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                                   package=imio.pm.wsclient,
                                   name='WS4PMCLIENT_ZCML')

WS4PMCLIENT_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, WS4PMCLIENT_ZCML),
                                       name='WS4PMCLIENT_Z2')

WS4PMCLIENT = PloneWithPackageLayer(
    zcml_filename="testing-settings.zcml",
    zcml_package=imio.pm.wsclient,
    additional_z2_products=('imio.dashboard',
                            'imio.pm.wsclient',
                            'imio.pm.ws',
                            'Products.PasswordStrength'),
    gs_profile_id='imio.pm.wsclient:testing',
    name="WS4PMCLIENT")

WS4PMCLIENT_PM_TESTING_PROFILE = WSCLIENTLayer(
    bases=(WS4PMCLIENT, ),
    zcml_filename="testing.zcml",
    zcml_package=imio.pm.wsclient,
    additional_z2_products=('imio.dashboard',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'imio.pm.wsclient',
                            'imio.pm.ws',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.PloneMeeting:testing',
    name="WS4PMCLIENT_PM_TESTING_PROFILE")

WS4PMCLIENT_PM_TESTING_PROFILE_INTEGRATION = IntegrationTesting(
    bases=(WS4PMCLIENT_PM_TESTING_PROFILE,), name="WS4PMCLIENT_PM_TESTING_PROFILE_INTEGRATION")

WS4PMCLIENT_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(WS4PMCLIENT,), name="WS4PMCLIENT_PROFILE_FUNCTIONAL")

WS4PMCLIENT_PM_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(WS4PMCLIENT_PM_TESTING_PROFILE, z2.ZSERVER), name="WS4PMCLIENT_PM_TESTING_PROFILE_FUNCTIONAL")
