from zope.app.component.hooks import getSite
from zope.component import queryMultiAdapter
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from collective.simplesocial.likebutton.interfaces import IOpenGraphProvider
from collective.simplesocial.likebutton.likebutton import likebutton_enabled

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
        
        # Get the name of the logo image from base_properties.
        portal = getSite()
        base_props = portal.restrictedTraverse('base_properties')
        logo_name = getattr(base_props, 'logoName', None)
        og_image = '/'.join([portal.absolute_url(), logo_name, 
            '@@facebook-thumbnail'])
        
        # Set the type of object.
        context_state = self.context.restrictedTraverse('@@plone_context_state')
        og_type = 'article'
        if context_state.is_portal_root():
            og_type = 'website'
        
        return {
            'og:title': self.context.Title(),
            'og:type': og_type,
            'og:image': og_image,
            'og:url': self.context.absolute_url(),
        }

class OpenGraphViewlet(common.ViewletBase):
    """
    Viewlet for displaying OpenGraph meta tags.
    """
    
    index = ViewPageTemplateFile('opengraph.pt')
    
    def update(self):
        self.available = likebutton_enabled(self.context)
        if not self.available:
            return
            
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
            
            
        
        