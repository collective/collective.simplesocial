from collective.googleanalytics.tracking import AnalyticsBaseTrackingPlugin
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

class FeedFormTracking(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track submission of the feed form.
    """
    
    __call__ = ViewPageTemplateFile('feedform.pt')