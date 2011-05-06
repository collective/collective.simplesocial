from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.formlib import form
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from collective.simplesocial import simplesocialMessageFactory as _

class IFacebookFanBox(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    href = schema.TextLine(
        title = _(u'Facebook Page URL'),
        description = _(u'Enter the URL of the Facebook page.'),
        )
        
    width = schema.Int(
        title = _(u'Width'),
        description = _(u'Enter the width of the box in pixels.'),
        min = 0,
        default = 200,
        )
        
    height = schema.Int(
        title = _(u'Height'),
        description = _(u'Enter the height of the box in pixels, or leave this'
            u' field blank for automatic sizing.'),
        min = 0,
        required = False,
        )
        
    colorscheme = schema.Choice(
        title = _(u'Color Scheme'),
        vocabulary = SimpleVocabulary.fromItems([
            (_(u'Light'), u'light'),
            (_(u'Dark'), u'dark'),
        ]),
        default = u'light',
    )
        
    show_faces = schema.Bool(
        title = _(u'Display faces'),
        description = _(u'Displays profile pictures of users who like the page.'),
        default = True,
        )
        
    show_stream = schema.Bool(
        title = _(u'Display stream'),
        description = _(u'Displays the public activity stream for the page.'),
        default = True,
        )
    
    show_header = schema.Bool(
        title = _(u'Display header'),
        description = _(u'Displays the header "Find us on Facebook."'),
        default = True,
        )

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFacebookFanBox)
    
    href = u''
    width = 200
    height = None
    colorscheme = u'light'
    show_faces = True
    show_stream = True
    show_header = True

    def __init__(self, href=u'', width=200, height=None, colorscheme=u'light',
        show_faces=True, show_stream=True, show_header=True):
        self.href = href
        self.width = width
        self.height = height
        self.colorscheme = colorscheme
        self.show_faces = show_faces
        self.show_stream = show_stream
        self.show_header = show_header

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Facebook Like Box"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('facebookfanbox.pt')


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IFacebookFanBox)

    def create(self, data):
        return Assignment(**data)
        
    def render(self):
        # make sure application ID is configured
        pprop = getToolByName(self.context, 'portal_properties')
        app_id = getattr(pprop.fb_properties, 'app_id', None)
        if not app_id:
            portal_url = getToolByName(self.context, 'portal_url')()
            IStatusMessage(self.request).addStatusMessage(_(u'You must configure your '
                u'Facebook Application ID before you can add a Like Box portlet.'))
            return self.request.RESPONSE.redirect(portal_url + '/@@facebook-settings')
        
        return base.AddForm.render(self)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFacebookFanBox)
