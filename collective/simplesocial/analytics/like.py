from collective.googleanalytics.tracking import AnalyticsBaseTrackingPlugin
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

class LikeTracking(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track likes and unlikes.
    """
    
    __call__ = ViewPageTemplateFile('like.pt')