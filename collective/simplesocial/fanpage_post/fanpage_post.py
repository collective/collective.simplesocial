from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collective.simplesocial.feedform.facebookfeedform import IFeedFormDataProvider
from collective.simplesocial.utils import json_serialize

class FanPagePostView(BrowserView):
    
    def attachment(self):
        data_provider = IFeedFormDataProvider(self.context)
        return json_serialize(data_provider.getAttachment())