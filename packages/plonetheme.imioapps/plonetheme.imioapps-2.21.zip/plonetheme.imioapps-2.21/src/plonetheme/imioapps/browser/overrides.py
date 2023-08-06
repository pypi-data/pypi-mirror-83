# -*- coding: utf-8 -*-

from plone.app.layout.globals.context import ContextState


class ImioContextState(ContextState):
    """ """

    def canonical_object_url(self):
        """Do not include portal_factory in URL."""
        url = super(ImioContextState, self).canonical_object_url()
        if 'portal_factory' in url:
            portal_factory_index = url.index('portal_factory')
            url = url[:portal_factory_index]
        return url
