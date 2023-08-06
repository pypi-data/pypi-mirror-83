# -*- coding: utf-8 -*-

from plone.app.textfield import RichText
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


from cpskin.locales import CPSkinMessageFactory as _


class IProduct(model.Schema):
    """ Marker interface and Dexterity Python Schema for Product
    """

    price = schema.TextLine(
        title=_(u'Price'),
        required=False
    )

    color = schema.Text(
        title=_(u'Color(s)'),
        required=False
    )

    size = schema.Text(
        title=_(u'Size(s)'),
        required=False
    )

    informations = RichText(
        title=_(u'Informations'),
        required=False
    )


@implementer(IProduct)
class Product(Container):
    """
    """
