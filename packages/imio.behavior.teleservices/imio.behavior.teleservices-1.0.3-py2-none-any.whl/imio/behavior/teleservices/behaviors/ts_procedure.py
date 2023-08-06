# -*- coding: utf-8 -*-

from imio.behavior.teleservices import _
from plone import schema
from plone.autoform import directives
from imio.behavior.teleservices.widgets import SelectProcedureWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class ITsProcedure(model.Schema):
    """
    """
    directives.widget("procedures", SelectProcedureWidget)
    procedures = schema.Choice(
        vocabulary="imio.behavior.teleservices.vocabularies.remote_procedures",
        title=_(u"E-Guichet procedures"),
        required=False,
        default=None
    )
