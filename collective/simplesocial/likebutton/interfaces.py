from zope.interface import Interface

class ILikeButtonEnabled(Interface):
    """
    Marker interface to enable the Facebook Like button.
    """
    
class ILikeButtonDisabled(Interface):
    """
    Marker interface to disable the Facebook Like button.
    """
    
class IOpenGraphProvider(Interface):
    """
    An adapter that provides the Open Graph metadata based on the current
    context and request.
    """
    
    def getProperties():
        """
        Returns a dictionary that maps Open Graph properties names
        (e.g. "og:title") to values.
        """