from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from collective.simplesocial.utils import json_serialize

class FBInitViewlet(ViewletBase):
    index = ViewPageTemplateFile('fb_init.pt')
    init_options = ''

    def update(self):
        super(FBInitViewlet, self).update()
        self.init_options = json_serialize(self._getInitOptions())
        
    def _getInitOptions(self):
        """
        Returns a Python dictionary containing the initialization options
        to be used when loading the Facebook API.
        """
        
        pprops = getToolByName(self.context, 'portal_properties')
        
        init_options = {
            'status': True,
            'cookie': True,
            'xfbml': True,
        }
        
        fb_properties = pprops.get('fb_properties', None)
        if fb_properties:
            app_id = fb_properties.getProperty('app_id')
            if app_id:
                init_options['appId'] = app_id
                
        return init_options
        

