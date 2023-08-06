# -*- coding: utf-8 -*-

from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from collective.z3cform.select2.widget.widget import ISingleSelect2Widget
from collective.z3cform.select2.widget.widget import SingleSelect2Widget


class ISelectProcedureWidget(ISingleSelect2Widget):
    """Marker interface for the SelectProcedureWidget"""


@implementer(ISelectProcedureWidget)
class SelectProcedureWidget(SingleSelect2Widget):
    noconfig_template = ViewPageTemplateFile("browser/templates/no_config.pt")
    badconfig_template = ViewPageTemplateFile("browser/templates/bad_config.pt")
    display_template = ViewPageTemplateFile("browser/templates/select_display.pt")

    def render(self):
        url = api.portal.get_registry_record("procedures.url_formdefs_api")
        if not url or url == "":
            return self.noconfig_template(self)
        elif self.items is not None and len(self.items) <= 1:
            return self.badconfig_template(self)

        if self.mode == "display":
            return self.display_template(self)

        return super(SelectProcedureWidget, self).render()
