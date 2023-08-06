# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone.app.contenttypes.behaviors.leadimage import ILeadImage


class ProductView(BrowserView):
    """
    """

    def available(self):
        scale_context = ILeadImage(self.context)
        return True if scale_context.image else False
