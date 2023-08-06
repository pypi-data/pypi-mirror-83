# -*- coding: utf-8 -*-

from plone import api
import logging

from cpskin.theme.upgradehandlers import upgrade_to_less as base_less_upgrade

logger = logging.getLogger('cpskin.diazotheme.trendy')


def upgrade_to_less(context):
    portal = api.portal.get()
    if not 'portal_less' in portal.objectIds():
        base_less_upgrade(context)
    context.runImportStepFromProfile(
        'profile-cpskin.diazotheme.trendy:default',
        'lessregistry'
    )
    logger.info('LESS files installed and configurations done !')


def migrate_carousel_sliders_to_count(context):
    index_collections_brains = api.content.find(
        portal_type='Collection',
        object_provides='cpskin.core.behaviors.indexview.ICpskinIndexViewSettings',
    )
    for brain in index_collections_brains:
        obj = brain.getObject()
        display_type = getattr(obj, 'display_type') or ''
        if display_type == 'slider-with-carousel':
            obj.display_type = 'slider-without-images'
