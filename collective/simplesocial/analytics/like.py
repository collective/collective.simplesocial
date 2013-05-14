from collective.googleanalytics.tracking import AnalyticsBaseTrackingPlugin
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class LikeTracking(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track likes and unlikes.
    """
    
    __call__ = ViewPageTemplateFile('like.pt')
