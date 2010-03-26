from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.simplesocial.feedform.facebookfeedform import IFeedFormDataProvider
from collective.simplesocial.utils import json_serialize

class FanPagePostView(BrowserView):
    
    def attachment(self):
        data_provider = IFeedFormDataProvider(self.context)
        return json_serialize(data_provider.getAttachment())
    
    @property
    def actor_id(self):
        ptool = getToolByName(self.context, 'portal_properties')
        page_id = ptool.fb_properties.getProperty('page_id')
        if page_id is not None:
            return json_serialize(page_id)
        return 'null'
