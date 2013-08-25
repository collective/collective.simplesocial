# -*- encoding: utf-8 -*-
from zope.interface import implements
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.site.hooks import getSite
from collective.simplesocial.browser.interfaces import IFacebookImage

class DefaultFacebookImage(object):
    """
    Retrieves the Facebook image for the object, or the default image.
    """
    
    implements(IFacebookImage)
    
    def __init__(self, context):
        self.context = context
        
    def _getDefault(self):
        """
        Returns the default image, in this case a scaled version of the logo.
        """
        
        portal = getSite()
        base_props = portal.restrictedTraverse('base_properties')
        logo_name = getattr(base_props, 'logoName', None)
        if logo_name:
            return '/'.join([portal.absolute_url(), logo_name,
                '@@facebook-thumbnail'])
        return None
    
    def getURL(self, scale='tile'):
        """
        Returns the URL of the scaled image.
        """
        
        scale_name = 'image_%s' % scale
        scaled_image = self.context.restrictedTraverse(scale_name, None)
        if scaled_image:
            return '%s/%s' % (self.context.absolute_url(), scale_name)
        return self._getDefault()
