from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from collective.simplesocial.utils import json_serialize

class FBInitViewlet(ViewletBase):
    index = ViewPageTemplateFile('fb_init.pt')
    init_options = ''

    def update(self):
        super(FBInitViewlet, self).update()
        self.settings = json_serialize(self._getSettings())
        
    def _getSettings(self):
        """
        Returns a Python dictionary containing the initialization options
        to be used when loading the Facebook API.
        """
        
        pprops = getToolByName(self.context, 'portal_properties')
        fb_properties = pprops.get('fb_properties', None)
        items = fb_properties.propertyItems()
        return dict([prop for prop in items \
            if not prop[0] == 'title' and not prop[1] == ''])
