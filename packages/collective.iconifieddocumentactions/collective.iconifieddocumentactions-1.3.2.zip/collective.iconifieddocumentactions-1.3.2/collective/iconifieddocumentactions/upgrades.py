# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.browserlayer.utils import unregister_layer


def move_to_collective_iconifieddocumentactions(context):
    context.runAllImportStepsFromProfile('profile-collective.iconifieddocumentactions:default')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    # remove old registered skin
    if hasattr(portal.portal_skins, 'iconifieddocumentactions_styles'):
        portal.portal_skins.manage_delObjects(ids=['iconifieddocumentactions_styles', ])
    # remove old registered CSS, does not fail if resource not exists
    portal.portal_css.unregisterResource('iconifieddocumentactions.css')
    # unregister old BrowserLayer 'communesplone.iconified_document_actions.layer'
    try:
        unregister_layer('communesplone.iconified_document_actions.layer')
    except KeyError:
        # layer was already unregistered, we pass...
        pass
