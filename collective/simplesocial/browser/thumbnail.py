from PIL import Image
from StringIO import StringIO
from zope.publisher.browser import BrowserPage
from plone.memoize import ram

def _makeFBThumbnail_cachekey(method, instance, size=(90, 90)):
    """
    Cache key for the makeFBThumbnail method.
    """
    context = instance.context
    return (context.getPhysicalPath(), context.modified(), size)

class FacebookThumbnail(BrowserPage):
    """
    Generate a thumbnail of the image for Facebook.
    """
    
    def __call__(self):
        """
        Return the scaled image.
        """
        self.request.RESPONSE.setHeader('Content-Type','image/jpeg')
        return self.makeFBThumbnail()
    
    @ram.cache(_makeFBThumbnail_cachekey)
    def makeFBThumbnail(self, size=(90, 90)):
        """
        Create the thumbnail no larger than 90 x 90 pixels.
        """

        image_file = StringIO(self.context.index_html(self.request, self.request.RESPONSE))
        image = Image.open(image_file)
        image = image.convert('RGB')
        image.thumbnail(size, Image.ANTIALIAS)
        output = StringIO()
        image.save(output, "JPEG")
        return output.getvalue()