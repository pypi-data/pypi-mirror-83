# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.textfield.interfaces import IRichText
from plone.app.textfield.value import RichTextValue
from plone.namedfile.file import NamedBlobImage
from Products.CMFPlone.utils import safe_unicode
from z3c.relationfield.relation import RelationValue
from zope import component
from zope.intid.interfaces import IIntIds
from zope.schema import getFieldsInOrder

import copy
import logging
import Missing
import unidecode


logger = logging.getLogger("cpskin.contenttypes")


def post_install(context):
    """We need to migrate existing TTW content types if any"""
    migrate_product(context)
    migrate_procedures(context)


def get_brains():
    # Récupérer les mots clés "je trouve"
    # types to migrate
    portal_types = api.portal.get_tool(name="portal_types")
    existing_brains = []
    if "demarche" in portal_types:
        existing_brains = api.content.find(portal_type="demarche")
    else:
        existing_document_brains = api.content.find(portal_type="Document")
        for brain in existing_document_brains:
            if brain.isearchTags == Missing.Value or brain.isearchTags is None:
                continue
            for tag in brain.isearchTags:
                if "DEMARCHE" in unidecode.unidecode(safe_unicode(tag)).upper():
                    existing_brains.append(brain)
    return existing_brains


def migrate_procedures(context):
    # keywords (DEMARCHE)
    # history_for_related_items = []
    portal_types = api.portal.get_tool(name="portal_types")
    existing_brains = []
    # new type Procedure.
    if "Procedure" not in portal_types:
        context.runImportStepFromProfile(
            "profile-cpskin.contenttypes:default", "typeinfo"
        )

    existing_brains = get_brains()

    for brain in existing_brains:
        old_procedure = brain.getObject()
        container = old_procedure.aq_parent
        # No procedure in PloneSite root
        # In each site, there is a document with a keyword
        # "démarche administrative" that stores the keyword.
        if INavigationRoot.providedBy(container):
            continue
        new_id = old_procedure.id
        temp_id = "new-{0}".format(new_id)
        # new type "Procedure"
        if portal_types.get("Procedure") not in container.allowedContentTypes():
            container.locally_allowed_types.append("Procedure")
            # container.allowedContentTypes().append(portal_types.get("Procedure"))
        new_procedure = api.content.create(
            container=container,
            type="Procedure",
            id=temp_id,
            title=old_procedure.Title(),
            safe_id=False,
        )
        new_procedure.description = old_procedure.Description()
        if hasattr(old_procedure, "e_guichet"):
            new_procedure.e_guichet = old_procedure.e_guichet
        if hasattr(old_procedure, "text"):
            if old_procedure.text is not None:
                new_procedure.text = RichTextValue(
                    raw=old_procedure.text.raw,
                    mimeType=old_procedure.text.mimeType,
                    outputMimeType=old_procedure.text.outputMimeType,
                )
        elif hasattr(old_procedure, "texte"):
            if old_procedure.texte is not None:
                new_procedure.text = RichTextValue(
                    raw=old_procedure.texte.raw,
                    mimeType=old_procedure.texte.mimeType,
                    outputMimeType=old_procedure.texte.outputMimeType,
                )
        elif hasattr(old_procedure, "contenu"):
            if old_procedure.contenu is not None:
                new_procedure.text = RichTextValue(
                    raw=old_procedure.contenu.raw,
                    mimeType=old_procedure.contenu.mimeType,
                    outputMimeType=old_procedure.contenu.outputMimeType,
                )
        else:
            # find RichText on "demarche" (old_procedure)
            # get first and set into new_procedure.text
            attr = None
            if "demarche" in portal_types:
                dem = portal_types["demarche"]
                fields = getFieldsInOrder(dem.lookupSchema())
                for name, field in fields:
                    if IRichText.providedBy(field):
                        attr = name
                        break
            if attr is not None:
                if old_procedure.__dict__.get(attr) is not None:
                    new_procedure.text = RichTextValue(
                        raw=old_procedure.__dict__.get(attr).raw,
                        mimeType=old_procedure.__dict__.get(attr).mimeType,
                        outputMimeType=old_procedure.__dict__.get(attr).outputMimeType,
                    )
        new_procedure.effective_date = old_procedure.effective_date
        new_procedure.creation_date = old_procedure.creation_date
        modification_date = old_procedure.modification_date
        new_procedure.workflow_history = old_procedure.workflow_history
        new_procedure.creators = old_procedure.creators
        new_procedure.language = old_procedure.language
        if hasattr(old_procedure, "hiddenTags"):
            new_procedure.hiddenTags = copy.deepcopy(old_procedure.hiddenTags)
        if hasattr(old_procedure, "iamTags"):
            new_procedure.iamTags = copy.deepcopy(old_procedure.iamTags)
        if hasattr(old_procedure, "isearchTags"):
            new_procedure.isearchTags = copy.deepcopy(old_procedure.isearchTags)
        if hasattr(old_procedure, "standardTags"):
            new_procedure.standardTags = copy.deepcopy(old_procedure.standardTags)

        # restore workflow state
        state = api.content.get_state(old_procedure)
        api.content.transition(obj=new_procedure, to_state=state)

        new_procedure.reindexObject()

        wf = new_procedure.portal_workflow.getWorkflowsFor(new_procedure)[0]
        wf.updateRoleMappingsFor(new_procedure)
        new_procedure.reindexObject()

        new_procedure.modification_date = modification_date
        new_procedure.reindexObject(idxs=["modified"])
        logger.info("Migrated procedure {0}".format(new_procedure.absolute_url()))

    get_related_items()
    # Remove old procedures after conversion process
    # because of old procedures relatedItems !
    remove_old_procedures()
    if "demarche" in portal_types:
        del portal_types["demarche"]


def get_related_items():
    existing_brains = get_brains()
    for brain in existing_brains:
        old_procedure = brain.getObject()
        container = old_procedure.aq_parent
        if INavigationRoot.providedBy(container):
            continue
        new_procedure = container.restrictedTraverse(
            "{}/{}".format(
                "/".join(container.getPhysicalPath()),
                "new-{}".format(old_procedure.getId()),
            )
        )
        if hasattr(old_procedure, "relatedItems") and old_procedure.relatedItems != []:
            for rel in old_procedure.relatedItems:
                if (
                    rel.to_object is not None
                    and rel.to_object.getTypeInfo().getId() == "demarche"
                ):
                    intids = component.getUtility(IIntIds)
                    relobj = rel.to_object
                    re = relobj.aq_parent.restrictedTraverse(
                        "{}/{}".format(
                            "/".join(relobj.aq_parent.getPhysicalPath()),
                            "new-{}".format(relobj.getId()),
                        )
                    )
                    old_procedure.relatedItems.append(RelationValue(intids.getId(re)))
                    old_procedure.relatedItems.remove(rel)
                    new_procedure.relatedItems = copy.deepcopy(
                        old_procedure.relatedItems
                    )
                    logger.info(
                        "{0} lien vers {1}".format(
                            new_procedure.absolute_url(), re.absolute_url()
                        )
                    )
        new_procedure.reindexObject()


def remove_old_procedures():
    existing_brains = get_brains()
    for brain in existing_brains:
        old_procedure = brain.getObject()
        container = old_procedure.aq_parent
        if INavigationRoot.providedBy(container):
            continue
        new_procedure = container.restrictedTraverse(
            "{}/{}".format(
                "/".join(container.getPhysicalPath()),
                "new-{}".format(old_procedure.getId()),
            )
        )
        new_id = new_procedure.getId().replace("new-", "")
        api.content.delete(obj=old_procedure, check_linkintegrity=True)
        api.content.rename(obj=new_procedure, new_id=new_id, safe_id=True)


def migrate_product(context):
    """Existing TTW 'produit' content type migration"""
    portal_types = api.portal.get_tool(name="portal_types")
    if "produit" not in portal_types:
        return

    existing_brains = api.content.find(portal_type="produit")
    for brain in existing_brains:
        old_product = brain.getObject()
        container = old_product.aq_parent
        new_id = old_product.id
        temp_id = "new-{0}".format(new_id)
        new_product = api.content.create(
            container=container,
            type="Product",
            id=temp_id,
            title=old_product.Title(),
            safe_id=False,
        )

        # copy standard fields / values
        new_product.description = old_product.Description()
        new_product.price = old_product.prix
        new_product.size = old_product.taille_s
        new_product.color = old_product.couleur_s
        if old_product.informations:
            new_product.informations = RichTextValue(
                raw=old_product.informations.raw,
                mimeType=old_product.informations.mimeType,
                outputMimeType=old_product.informations.outputMimeType,
            )
        new_product.effective_date = old_product.effective_date
        new_product.creation_date = old_product.creation_date
        modification_date = old_product.modification_date
        new_product.workflow_history = old_product.workflow_history
        new_product.creators = old_product.creators
        new_product.language = old_product.language

        # copy leadimage
        old_image = old_product.image
        if old_image:
            filename = old_image.filename
            old_image_data = old_image.data
            namedblobimage = NamedBlobImage(data=old_image_data, filename=filename)
            setattr(new_product, "image", namedblobimage)

        # restore workflow state
        state = api.content.get_state(old_product)
        api.content.transition(obj=new_product, to_state=state)

        api.content.delete(obj=old_product, check_linkintegrity=True)
        api.content.rename(obj=new_product, new_id=new_id, safe_id=True)
        new_product.reindexObject()

        wf = new_product.portal_workflow.getWorkflowsFor(new_product)[0]
        wf.updateRoleMappingsFor(new_product)
        new_product.reindexObject()

        new_product.modification_date = modification_date
        new_product.reindexObject(idxs=["modified"])

        logger.info("Migrated product {0}".format(new_product.absolute_url()))

    del portal_types["produit"]
