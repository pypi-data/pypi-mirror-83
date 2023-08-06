# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IconifiedDocumentActionsViewlet(ViewletBase):
    def update(self):
        super(IconifiedDocumentActionsViewlet, self).update()

        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.actions = self.context_state.actions('document_actions')

    index = ViewPageTemplateFile("iconified_document_actions.pt")
