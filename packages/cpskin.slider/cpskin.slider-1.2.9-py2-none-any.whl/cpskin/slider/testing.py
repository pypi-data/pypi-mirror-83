# -*- coding: utf-8 -*-

from cpskin.core.interfaces import IFolderViewSelectedContent
from plone import api
from plone.testing import z2
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import applyProfile
from plone.app.testing import (login,
                               TEST_USER_NAME,
                               setRoles,
                               TEST_USER_ID)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from zope.interface import alsoProvides

import cpskin.slider


class CPSkinSliderPloneWithPackageLayer(PloneWithPackageLayer):
    """
    """
    def setUpZope(self, app, configurationContext):
        super(CPSkinSliderPloneWithPackageLayer, self).setUpZope(
            app,
            configurationContext
        )
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        applyProfile(portal, 'cpskin.slider:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        slider_folder = api.content.create(
            type='Folder',
            title='Slider Folder',
            id='slider-folder',
            description='Mon slider folder',
            container=portal)
        slider_folder.setLayout('folderview')
        api.content.transition(obj=slider_folder, transition='publish')
        news1 = api.content.create(
            type='News Item',
            title='Foire aux boudins',
            id='1-foire-aux-boudins',
            description='Superbe foire',
            container=slider_folder)
        api.content.transition(obj=news1, transition='publish')
        news2 = api.content.create(
            type='News Item',
            title='Festival de danse folklorique',
            id='2-festival-de-danse-folklorique',
            description='Parfois synonyme de danse folklorique ou de danse traditionnelle...',  # noqa
            container=slider_folder)
        api.content.transition(obj=news2, transition='publish')
        event = api.content.create(
            type='Event',
            title='Evénement important',
            id='3-evenement-important',
            description='Un événement important va se produire...',
            container=slider_folder)
        api.content.transition(obj=event, transition='publish')
        collection = api.content.create(
            type='Collection',
            title='SliderCollection',
            container=slider_folder)
        api.content.transition(obj=collection, transition='publish')
        collection.display_type = 'slider-with-carousel'
        alsoProvides(collection, IFolderViewSelectedContent)
        catalog = api.portal.get_tool('portal_catalog')
        catalog.reindexObject(collection)
        query = [{'i': 'Type',
                  'o': 'plone.app.querystring.operation.string.is',
                  'v': ['News Item', 'Event'],
                  }]
        collection.setQuery(query)
        collection.setSort_on('getId')
        api.portal.set_registry_record('cpskin.core.interfaces.ICPSkinSettings.auto_play_slider', False)  # noqa


CPSKIN_SLIDER_FIXTURE = CPSkinSliderPloneWithPackageLayer(
    name='CPSKIN_SLIDER_FIXTURE',
    zcml_filename='testing.zcml',
    zcml_package=cpskin.slider)


CPSKIN_SLIDER_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_SLIDER_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='cpskin.slider:Robot')
