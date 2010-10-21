from Acquisition import aq_inner, aq_parent
from Products.PloneFormGen.interfaces import IPloneFormGenForm
from collective.simplesocial.feedform.facebookfeedform import \
    DefaultFeedFormDataProvider
    
class ThanksPageDataProvider(DefaultFeedFormDataProvider):
    """
    An adapter that provides the feed form settings for PloneFormGen thank you
    pages. It gets the attachment information from the form rather than the
    thank you page.
    """
    
    def __init__(self, context):
        parent = aq_parent(aq_inner(context))
        if IPloneFormGenForm.providedBy(parent):
            self.context = parent
        else:
            self.context = context