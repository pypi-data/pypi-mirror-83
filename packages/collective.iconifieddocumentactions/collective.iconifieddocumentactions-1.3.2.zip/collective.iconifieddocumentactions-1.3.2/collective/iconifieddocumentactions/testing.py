# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
import collective.iconifieddocumentactions
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from plone.testing import z2


FIXTURE = PloneWithPackageLayer(
    zcml_filename="configure.zcml",
    zcml_package=collective.iconifieddocumentactions,
    additional_z2_products=[],
    gs_profile_id='collective.iconifieddocumentactions:default',
    name="collective.iconifieddocumentactions:FIXTURE")

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="collective.iconifieddocumentactions:Integration")

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="collective.iconifieddocumentactions:Functional")

ROBOT = FunctionalTesting(
    bases=(FIXTURE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ROBOT")
