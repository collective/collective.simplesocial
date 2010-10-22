from zope.interface import Interface
from zope import schema
from collective.simplesocial import simplesocialMessageFactory as _

class IBrowserLayer(Interface):
    """
    Marker interface for this product's browser layer.
    """

class IFacebookSettingsForm(Interface):
    """
    Marker interface for the Facebook Settings form. It prevents the normal
    Facebook initialization sequence from taking place so that we can check to
    make sure we have a valid application ID.
    """

class IFacebookSettings(Interface):

    app_id = schema.TextLine(
        title = _(u'Application ID'),
        description = _(u'Enter the application ID for your Facebook application.'),
    )

    page_id = schema.ASCIILine(
        title = _(u'Fan Page'),
        description = _(u"Select the fan page you want to post to."),
        required = False,
    )