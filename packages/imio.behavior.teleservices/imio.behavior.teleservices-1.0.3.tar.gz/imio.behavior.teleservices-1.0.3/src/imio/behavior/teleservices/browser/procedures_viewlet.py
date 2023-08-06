# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import logging


logger = logging.getLogger("imio.behavior.teleservices viewlet")


class ProceduresViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('templates/procedures_viewlet.pt')

    def get_selected_procedure_title(self):
        pass
