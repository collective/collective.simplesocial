from Products.Five.browser import BrowserView
from collective.simplesocial.feedform.facebookfeedform import IFeedFormDataProvider
from collective.simplesocial import json

class FanPagePostView(BrowserView):
    
    def attachment(self):
        data_provider = IFeedFormDataProvider(self.context)
        return json.dumps(data_provider.getAttachment())