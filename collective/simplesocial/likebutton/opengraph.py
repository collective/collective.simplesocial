# -*- encoding: utf-8 -*-
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.site.hooks import getSite
from zope.component import queryMultiAdapter
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from collective.simplesocial.browser.interfaces import IFacebookSettings, \
    IFacebookImage
from collective.simplesocial.likebutton.interfaces import IOpenGraphProvider
from collective.simplesocial.likebutton.likebutton import likebutton_enabled, \
    likebutton_available

class DefaultOpenGraphProvider(object):
    """
    An adapter that provides Open Graph metadata based on the current
    context and request.
    """
    
    implements(IOpenGraphProvider)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def getProperties(self):
        """
        Returns a dictionary that maps Open Graph properties names
        (e.g. "og:title") to values.
        """
        
        result = {}
        
        # Set the type of object.
        context_state = self.context.restrictedTraverse('@@plone_context_state')
        portal = getSite()
        settings = IFacebookSettings(portal)
        
        if context_state.is_portal_root():
            result['og:type'] = 'website'
            portal = getSite()
            result['og:title'] = portal.Title()
            result['og:url'] = portal.absolute_url()
            description = portal.Description()
            
        else:
            result['og:type'] = 'article'
            result['og:title'] = self.context.Title()
            result['og:url'] = self.context.absolute_url()
            description = self.context.Description()

        if description:
            result['og:description'] = description
        
        image_provider = IFacebookImage(self.context)
        image_url = image_provider.getURL(scale='preview')
        if image_url:
            result['og:image'] = image_url
            
        result['og:site_name'] = portal.Title()
        result['fb:app_id'] = settings.app_id
        
        return result

class OpenGraphViewlet(common.ViewletBase):
    """
    Viewlet for displaying OpenGraph meta tags.
    """
    
    index = ViewPageTemplateFile('opengraph.pt')
    
    def update(self):
        portal = getSite()
        settings = IFacebookSettings(portal)
        self.available = likebutton_available(settings) and \
            likebutton_enabled(self.context, settings)
            
        # First try to find an adapter with the same name as the content type.
        # Then fall back to a generic adapter.
        for name in [self.context.portal_type, '']:
            adapter = queryMultiAdapter(
                (self.context, self.request),
                interface=IOpenGraphProvider,
                name=name,
            )
            if adapter:
                self.og_properties = adapter.getProperties()
                return
            
        # We haven't found an adapter, so the viewlet should not be displayed.
        self.available = False
            
            
        
        
