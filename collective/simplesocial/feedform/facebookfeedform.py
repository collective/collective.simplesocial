from zope.interface import Interface, implements
from zope.app.component.hooks import getSite

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.simplesocial import simplesocialMessageFactory as _
from collective.simplesocial.utils import json_escape, json_serialize

class IFeedFormDataProvider(Interface):
    """
    Provides the data used to populate the Facebook feed form.
    """
    
    def getSettings(self, defaults):
        """
        Given an instance of Assignment containing the default settings,
        return an object providing IFacebookFeedForm.
        
        In implementing getSettings, be sure to copy the defaults object to avoid
        changing the portlet settings!
        """
        
    def getAttachment(self):
        """
        Return a dictionary containing the following keys that describe the
        feed form attachment:
            - name
            - href
            - description
            - media (a list containing dictionaries with these keys)
                - type
                - src
                - href
        """

class DefaultFeedFormDataProvider(object):
    """
    An adapter that provides the default feed form settings as specified in 
    the portlet if a content type-specific adapter is not found.
    """
    
    implements(IFeedFormDataProvider)
    
    def __init__(self, context):
        self.context = context
        
    def getSettings(self, defaults):
        return defaults

    def getAttachment(self):
        result = {
            'name': self.context.Title(),
            'href': self.context.absolute_url(),
        }
        if hasattr(self.context, 'Description') and self.context.Description():
            result.update({'description': ' '.join(self.context.Description().split())})
        try:
            self.context.restrictedTraverse('image_tile')
            result.update({
                'media': [{
                    'type': 'image',
                    'src': self.context.absolute_url() + '/image_tile',
                    'href': self.context.absolute_url(),
                }]
            })
        except (AttributeError, KeyError):
            portal = getSite()
            base_props = portal.restrictedTraverse('base_properties')
            logo_name = getattr(base_props, 'logoName', None)
            if logo_name:
                result.update({
                    'media': [{
                        'type': 'image',
                        'src': '/'.join([portal.absolute_url(), logo_name, '@@facebook-thumbnail']),
                        'href': self.context.absolute_url(),
                    }]
                })
        return result

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
        title = _(u'User Prompt'),
        description = _(u'This message will be displayed to the user, prompting them to '
                        u'publish a message to their feed.'),
        default = _(u'Please consider sharing with your friends.'),
        required = False,
        )
    
    user_message = schema.TextLine(
        title = _(u'User Message'),
        description = _(u'This will be used as the default text for the user-editable '
                        u'comment portion of the post.'),
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
                 action_link_text, action_link_href):
        self.action_title = action_title
        self.user_message_prompt = user_message_prompt
        self.user_message = user_message
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

    def __init__(self, context, request, view, manager, data):
        data_provider = IFeedFormDataProvider(context)
        data = data_provider.getSettings(data)
        self.attachment_data = data_provider.getAttachment()
        super(Renderer, self).__init__(context, request, view, manager, data)

    @property
    def attachment(self):
        result_dict = self.attachment_data.copy()
        if self.data.action_title:
            result_dict.update({'caption': '{*actor*} ' + self.data.action_title})
        return json_serialize(result_dict)

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
