from collective.googleanalytics.tracking import AnalyticsBaseTrackingPlugin
import os

class FeedFormTracking(AnalyticsBaseTrackingPlugin):
    """
    A tracking plugin to track submission of the feed form.
    """
    
    def __call__(self):
        """
        Renders the tracking plugin.
        """
        
        template_file = os.path.join(os.path.dirname(__file__), 'feedform.tpl')
        return self.render_file(template_file, {
            'relative_url': self.relative_url(),
        })