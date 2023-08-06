# -*- coding: utf-8 -*-
from plone import api

import logging


logger = logging.getLogger("cpskin.core")


def apply_new_default_view(context):
    catalog = api.portal.get_tool("portal_catalog")
    brains = catalog(
        {"object_provides": "cpskin.contenttypes.content.procedure.IProcedure"}
    )
    for brain in brains:
        obj = brain.getObject()
        obj.setLayout("procedure_view")
        obj.reindexObject()

def no_more_procedure_view(context):
    catalog = api.portal.get_tool("portal_catalog")
    brains = catalog(
        {"object_provides": "cpskin.contenttypes.content.procedure.IProcedure"}
    )
    for brain in brains:
        obj = brain.getObject()
        obj.setLayout("view")
        obj.reindexObject()
