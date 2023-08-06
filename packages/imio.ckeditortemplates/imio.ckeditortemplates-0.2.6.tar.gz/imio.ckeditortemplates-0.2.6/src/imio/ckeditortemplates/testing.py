# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import imio.ckeditortemplates


IMIO_CKEDITORTEMPLATES = PloneWithPackageLayer(
    zcml_package=imio.ckeditortemplates,
    zcml_filename='testing.zcml',
    gs_profile_id='imio.ckeditortemplates:testing',
    name='IMIO_CKEDITORTEMPLATES'
)

IMIO_CKEDITORTEMPLATES_INTEGRATION = IntegrationTesting(
    bases=(IMIO_CKEDITORTEMPLATES, ),
    name="IMIO_CKEDITORTEMPLATES_INTEGRATION"
)

IMIO_CKEDITORTEMPLATES_FUNCTIONAL = FunctionalTesting(
    bases=(IMIO_CKEDITORTEMPLATES, ),
    name="IMIO_CKEDITORTEMPLATES_FUNCTIONAL"
)

IMIO_CKEDITORTEMPLATES_ROBOT_TESTING = FunctionalTesting(
    bases=(IMIO_CKEDITORTEMPLATES,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="IMIO_CKEDITORTEMPLATES_ROBOT_TESTING")
