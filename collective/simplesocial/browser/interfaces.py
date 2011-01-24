from zope.interface import Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
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

class IFacebookImage(Interface):
    """
    Retrieves the Facebook image for the object, or the default image.
    """
    
    def getURL(scale):
        """
        Returns the URL of the scaled image.
        """

class IFacebookSettings(Interface):

    app_id = schema.TextLine(
        title = _(u'Application ID'),
        description = _(u'Enter the application ID for your'
            u' Facebook application.'),
    )
    
    post_to_page_available = schema.Bool(
        title = _(u"Allow site managers to post updates to a"
            u" Facebook Page"),
        default = True,
    )

    page_id = schema.ASCIILine(
        title = _(u'Page'),
        description = _(u"Select the Facebook Page you want to post to."),
        required = False,
    )
    
    like_button_available = schema.Bool(
        title = _(u"Display Like buttons on this site"),
        default = True,
    )
    
    like_button_types = schema.List(
        title = _(u'Content Types'),
        description = _(u"Display Like buttons on these content types"
            u" by default."),
        value_type = schema.Choice(
            vocabulary = 'plone.app.vocabularies.ReallyUserFriendlyTypes',
        ),
        default=['Document', 'Event', 'News Item'],
    )
    
    like_button_layout = schema.Choice(
        title = _(u'Layout'),
        vocabulary = SimpleVocabulary.fromItems([
            (_(u'Standard'), u'standard'),
            (_(u'Button Count'), u'button_count'),
            (_(u'Box Count'), u'box_count'),
        ]),
        default = u'standard',
    )
    
    like_button_show_faces = schema.Bool(
        title = _(u"Show Faces"),
        description = _(u"Display profile pictures beneath the Like button."),
        default = True,
    )
    
    like_button_width = schema.Int(
        title = _(u'Width'),
        description = _(u"Enter the width of the Like button area in pixels."),
        default = 450,
    )
    
    like_button_action = schema.Choice(
        title = _(u'Action'),
        description = _(u'Choose the verb to be displayed in the Like button.'),
        vocabulary = SimpleVocabulary.fromItems([
            (_(u'Like'), u'like'),
            (_(u'Recommend'), u'recommend'),
        ]),
        default = u'like',
    )
    
    like_button_font = schema.Choice(
        title = _(u'Font'),
        vocabulary = SimpleVocabulary.fromItems([
            (_(u'Default'), u''),
            (_(u'Arial'), u'arial'),
            (_(u'Lucida Grande'), u'lucida grande'),
            (_(u'Segoe UI'), u'segoe ui'),
            (_(u'Tahoma'), u'tahoma'),
            (_(u'Trebuchet MS'), u'trebuchet ms'),
            (_(u'Verdana'), u'verdana'),
        ]),
        default = u'',
    )
    
    like_button_color_scheme = schema.Choice(
        title = _(u'Color Scheme'),
        vocabulary = SimpleVocabulary.fromItems([
            (_(u'Light'), u'light'),
            (_(u'Dark'), u'dark'),
        ]),
        default = u'light',
    )
    
    like_button_ref = schema.ASCIILine(
        title = _(u'Referral Label'),
        max_length = 49,
        description = _(u'To track referrals from Facebook, enter the value'
            u' that will be used for the fb_ref parameter.'),
        required = False,
    )
    