# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
logger = logging.getLogger('imio.ckeditortemplates.upgrades')


def update_profile(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-imio.ckeditortemplates:default')
    logger.info("Upgrade step ran.")
