from Products.Five.browser import BrowserView
from collective.simplesocial.feedform.facebookfeedform import IFeedFormDataProvider
from collective.simplesocial.utils import json_serialize

class FanPagePostView(BrowserView):
    
    def attachment(self):
        # XXX update the default provider to add a utm_source and shorten the URL
        data_provider = IFeedFormDataProvider(self.context)
        return json_serialize(data_provider.getAttachment())
    
    @property
    def actor_id(self):
        # XXX look up from property sheet
        return json_serialize('103413989697471')
