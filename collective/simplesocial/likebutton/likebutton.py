# -*- encoding: utf-8 -*-
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.site.hooks import getSite
from zope.interface import alsoProvides, noLongerProvides
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.viewlets import common
from collective.simplesocial.browser.interfaces import IFacebookSettings
from collective.simplesocial.likebutton.interfaces import ILikeButtonEnabled, \
    ILikeButtonDisabled
from collective.simplesocial import simplesocialMessageFactory as _

def likebutton_available(settings):
    """
    Returns a boolean indicating whether the Like button is available globally.
    """
    
    if settings.like_button_available and settings.app_id:
        return True
    return False

def likebutton_enabled(context, settings):
    """
    Returns a boolean indicating whether the Like button is enabled for this
    content object.
    """
    
    if ILikeButtonDisabled.providedBy(context):
        # If Like buttons have been disabled for this content object, we 
        # shouldn't check anything else.
        return False
    
    # Check if this type is in the enabled types or if it has the enabled
    # marker interface.
    if context.portal_type in settings.like_button_types or \
        ILikeButtonEnabled.providedBy(context):
        return True
    return False

class LikeButtonViewlet(common.ViewletBase):
    """
    Viewlet that holds a Facebook Like button.
    """
    
    index = ViewPageTemplateFile('likebutton.pt')
    
    def update(self):
        self.settings = IFacebookSettings(getSite())
        self.available = likebutton_available(self.settings) and \
            likebutton_enabled(self.context, self.settings)
            
class ToggleLikeButton(BrowserView):
    """
    Browser view to turn the Like button on or off for this content object.
    """
        
    def _get_settings(self):
        portal = self.context.restrictedTraverse('@@plone_portal_state').portal()
        return IFacebookSettings(portal)
    
    def can_enable(self):
        """
        Returns a boolean indicating whether the Like button can be enabled
        for this type.
        """
        
        settings = self._get_settings()
        return likebutton_available(settings) and not \
            likebutton_enabled(self.context, settings)
        
    def can_disable(self):
        """
        Returns a boolean indicating whether the Like button can be disabled
        for this type.
        """
        
        settings = self._get_settings()
        return likebutton_available(settings) and \
            likebutton_enabled(self.context, settings)
    
    def __call__(self):
        
        # Decide whether we are enabling or disabling based on the request.
        enable = self.request.get('enable', False)
        settings = self._get_settings()

        if enable:
            if ILikeButtonDisabled.providedBy(self.context):
                noLongerProvides(self.context, ILikeButtonDisabled)
            if not self.context.portal_type in settings.like_button_types:
                alsoProvides(self.context, ILikeButtonEnabled)
            IStatusMessage(self.request).addStatusMessage(
                _(u'Like button enabled.'), type='info')
        else:
            if ILikeButtonEnabled.providedBy(self.context):
                noLongerProvides(self.context, ILikeButtonEnabled)
            if self.context.portal_type in settings.like_button_types:
                alsoProvides(self.context, ILikeButtonDisabled)
            IStatusMessage(self.request).addStatusMessage(
                _(u'Like button disabled.'), type='info')
                
        return self.request.RESPONSE.redirect(self.context.absolute_url())
