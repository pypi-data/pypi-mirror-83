from imio.behavior.teleservices.widgets import ISelectProcedureWidget
from plone.dexterity.browser.view import DefaultView


class ProcedureDisplay(DefaultView):

    def updateWidgets(self):
        super(ProcedureDisplay, self).updateWidgets()
        # Remove our widget if empty (otherwise we see label without value)
        for name, widget in self.widgets.items():
            if not ISelectProcedureWidget.providedBy(widget) or widget.value:
                continue
            del self.widgets[name]
