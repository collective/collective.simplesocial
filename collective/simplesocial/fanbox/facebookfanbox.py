from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from zope.schema.vocabulary import SimpleVocabulary
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.simplesocial import simplesocialMessageFactory as _

class IFacebookFanBox(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    profile_id = schema.TextLine(
        title = _(u'Profile ID'),
        description = _(u'Paste the ID of the Facebook Page that should be promoted.  You can find it at the end of the URL of the Page when viewing it in Facebook.  (Only Pages are supported; not Groups.)'),
        )
    
    stream = schema.Choice(
        title = _(u'Display stories in activity stream?'),
        vocabulary = SimpleVocabulary.fromItems((
            (_(u'yes'), 1),
            (_(u'no'), 0)
            )),
        default = 1,
        )
    
    connections = schema.Int(
        title = _(u'Connections'),
        description = _(u'The number of fans to display in the Fan Box. Specifying 0 hides the list of fans in the Fan Box. You cannot display more than 100 fans.'),
        min = 0,
        max = 100,
        default = 10,
        )
    
    width = schema.Int(
        title = _(u'Width'),
        description = _(u'Enter the desired width of the box, in pixels.'),
        min = 200,
        default = 200,
        )
    
    height = schema.Int(
        title = _(u'Height'),
        description = _(u'Enter the desired height of the box, in pixels.'),
        default = 554,
        )

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFacebookFanBox)

    def __init__(self, profile_id, stream, connections, width, height):
        self.profile_id = profile_id
        self.stream = stream
        self.connections = connections
        self.width = width
        self.height = height

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Facebook Fan Box"


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


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IFacebookFanBox)
