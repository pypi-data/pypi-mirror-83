from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.portlet.collection.collection import (Assignment as BaseCollectionPortletAssignment,
                                                ICollectionPortlet,
                                                Renderer as BaseCollectionPortletRenderer)
from zope.formlib import form
from zope.interface import implements
from cpskin.slider import messageFactory as _


class ISliderCollectionPortlet(ICollectionPortlet):
    """
        Collection portlet
    """


class Assignment(BaseCollectionPortletAssignment):
    implements(ISliderCollectionPortlet)


class Renderer(BaseCollectionPortletRenderer):

    render = ViewPageTemplateFile('slidercollectionportlet.pt')


class AddForm(base.AddForm):
    """
       add form
    """
    form_fields = form.Fields(ISliderCollectionPortlet)

    def create(self, data):
        return Assignment(**data)

    label = _(u"Collection portlet with slider view")
    description = _(u"add a collection portlet with slider view")

    form_fields = form.Fields(ISliderCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget


class EditForm(base.EditForm):
    """Portlet edit form."""
    form_fields = form.Fields(ISliderCollectionPortlet)

    label = _(u"Collection portlet with slider view")
    description = _(u"edit a collection portlet with slider view")

    form_fields = form.Fields(ISliderCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
