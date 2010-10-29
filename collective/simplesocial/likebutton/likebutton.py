from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from collective.simplesocial.likebutton.interfaces import ILikeButtonEnabled, \
    ILikeButtonDisabled

def likebutton_enabled(context):
    """
    Returns a boolean indicating whether the Like button is enabled for this
    content object.
    """
    
    pprops = getToolByName(context, 'portal_properties')
    fb_properties = pprops.get('fb_properties', None)
    enabled = fb_properties.getProperty('like_button_enabled', False)
    if not enabled or ILikeButtonDisabled.providedBy(context):
        # If Like buttons are not globally enabled, or if they've been
        # disabled for this content object, we shouldn't check anything else.
        return False
    
    # Check if this type is in the enabled types or if it has the enabled
    # marker interface.
    enabled_types = fb_properties.getProperty('like_button_types', [])
    if context.portal_type in enabled_types or \
        ILikeButtonEnabled.providedBy(context):
        return True
    return False

class LikeButtonViewlet(common.ViewletBase):
    """
    Viewlet that holds a Facebook Like button.
    """
    
    index = ViewPageTemplateFile('likebutton.pt')
    
    def update(self):
        self.available = likebutton_enabled(self.context)
        if not self.available:
            return
        
        pprops = getToolByName(self.context, 'portal_properties')
        fb_properties = pprops.get('fb_properties', None)
        
        self.layout = fb_properties.getProperty('like_button_layout', u'standard')
        self.show_faces = fb_properties.getProperty('like_button_show_faces', True)
        self.width = fb_properties.getProperty('like_button_width', 450)
        self.action = fb_properties.getProperty('like_button_action', u'like')
        self.font = fb_properties.getProperty('like_button_font', u'')
        self.color_scheme = fb_properties.getProperty('like_button_color_scheme',
            u'light')
        