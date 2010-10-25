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
        description = _(u'Enter the application ID for your'
            u' Facebook application.'),
    )
    
    post_to_page_enabled = schema.Bool(
        title = _(u"Allow site managers to post updates to a"
            u" Facebook Page"),
        default = True,
        required = False,
    )

    page_id = schema.ASCIILine(
        title = _(u'Page'),
        description = _(u"Select the Facebook Page you want to post to."),
        required = False,
    )
    
    like_button_enabled = schema.Bool(
        title = _(u"Display Like buttons on this site"),
        default = True,
        required = False,
    )
    
    like_button_types = schema.List(
        title = _(u'Content Types'),
        description = _(u"Display Like buttons on these content types"
            u" by default."),
        value_type = schema.Choice(
            vocabulary = 'plone.app.vocabularies.ReallyUserFriendlyTypes',
        ),
        required = False,
    )