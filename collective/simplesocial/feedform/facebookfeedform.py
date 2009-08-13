from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.simplesocial import simplesocialMessageFactory as _
from collective.simplesocial.utils import json_escape

class IFacebookFeedForm(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    action_title = schema.TextLine(
        title = _(u'Action Title'),
        description = _(u"A one-line message describing an action the user took. "
                        u"The user's name and a space will be added at the beginning."),
        default = _(u'took an action.')
        )
    
    user_message_prompt = schema.TextLine(
        title = _(u'User prompt'),
        description = _(u'This message will be displayed to the user, prompting them to '
                        u'publish a message to their feed.'),
        default = _(u'Please consider sharing with your friends.'),
        required = False,
        )
    
    user_message = schema.TextLine(
        title = _(u'User message'),
        description = _(u'This will be used as the default text for the user-editable '
                        u'comment portion of the post.'),
        required = False,
        missing_value = u'',
        )
    
    image_url = schema.TextLine(
        title = _(u'Image URL'),
        description = _(u'Paste the URL for an image to be included with the feed post. Optional.'),
        required = False,
        missing_value = u'',
        )
    
    image_link_href = schema.TextLine(
        title = _(u'Image Link URL'),
        description = _(u'URL for the webpage which the image should link to when clicked. Optional.'),
        required = False,
        missing_value = u'',
        )
    
    action_link_text = schema.TextLine(
        title = _(u'Action Link Text'),
        description = _(u'Text of a link which will be shown after the feed post. Optional.'),
        required = False,
        missing_value = u'',
        )
    
    action_link_href = schema.TextLine(
        title = _(u'Action Link URL'),
        description = _(u'URL target of the action link shown after the feed post.'),
        required = False,
        missing_value = u'',
        )

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFacebookFeedForm)

    image_url = u''
    image_link_href = u''
    action_link_text = u''
    action_link_href = u''

    def __init__(self, action_title, user_message_prompt, user_message, 
                 image_url, image_link_href, action_link_text, action_link_href):
        self.action_title = action_title
        self.user_message_prompt = user_message_prompt
        self.user_message = user_message
        self.image_url = image_url
        self.image_link_href = image_link_href
        self.action_link_text = action_link_text
        self.action_link_href = action_link_href

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Facebook Feed Form"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('facebookfeedform.pt')
    callback = 'function(res){}'

    @property
    def attachment(self):
        out = '{'
        out += '"caption": "{*actor*} ' + json_escape(self.data.action_title) + '"'
        if self.data.image_url:
            out += ', "media": [{"type": "image"'
            out += ', "src": "' + json_escape(self.data.image_url) + '"'
            out += ', "href": "' + json_escape(self.data.image_link_href) + '"}]'
        out += '}'
        return out

    @property
    def action_links(self):
        out = '['
        if self.data.action_link_text:
            out += '{"text": "' + json_escape(self.data.action_link_text) + '"'
            out += ', "href": "' + json_escape(self.data.action_link_href) + '"}'
        out += ']'
        return out

    @property
    def user_message_prompt(self):
        return json_escape(self.data.user_message_prompt)
    
    @property
    def user_message(self):
        return json_escape(self.data.user_message)

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IFacebookFeedForm)
    extra_script = "jq('input[type=text]').attr('size', '50');"

    def render(self):
        # make sure API Key is configured
        pprop = getToolByName(self.context, 'portal_properties')
        api_key = getattr(pprop.fb_properties, 'api_key', None)
        if not api_key:
            portal_url = getToolByName(self.context, 'portal_url')()
            IStatusMessage(self.request).addStatusMessage(_(u'You must configure your '
                u'Facebook API Key before you can add a Feed Form portlet.'))
            return self.request.RESPONSE.redirect(portal_url + '/@@facebook-settings')
        
        return base.AddForm.render(self)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFacebookFeedForm)
    extra_script = "jq('input[type=text]').attr('size', '50');"
