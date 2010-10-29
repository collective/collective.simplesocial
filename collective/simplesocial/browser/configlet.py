from zope.component import adapts
from zope.interface import implements
from z3c.form import form, field, group
from z3c.form.browser.checkbox import CheckBoxFieldWidget, \
    SingleCheckBoxFieldWidget
from plone.z3cform.layout import FormWrapper
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from collective.simplesocial.browser.interfaces import IFacebookSettingsForm, \
    IFacebookSettings
from collective.simplesocial import simplesocialMessageFactory as _

class FacebookSettingsAdapter(object):
    implements(IFacebookSettings)
    adapts(ISiteRoot)
    
    def __init__(self, context):
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.fb_properties
        self.encoding = pprop.site_properties.default_charset
        
    app_id = ProxyFieldProperty(IFacebookSettings['app_id'])
    post_to_page_available = ProxyFieldProperty(IFacebookSettings['post_to_page_available'])
    page_id = ProxyFieldProperty(IFacebookSettings['page_id'])
    like_button_available = ProxyFieldProperty(IFacebookSettings['like_button_available'])
    like_button_types = ProxyFieldProperty(IFacebookSettings['like_button_types'])
    like_button_layout = ProxyFieldProperty(IFacebookSettings['like_button_layout'])
    like_button_show_faces = ProxyFieldProperty(IFacebookSettings['like_button_show_faces'])
    like_button_width = ProxyFieldProperty(IFacebookSettings['like_button_width'])
    like_button_action = ProxyFieldProperty(IFacebookSettings['like_button_action'])
    like_button_font = ProxyFieldProperty(IFacebookSettings['like_button_font'])
    like_button_color_scheme = ProxyFieldProperty(IFacebookSettings['like_button_color_scheme'])

class ApplicationGroup(group.Group):
    """
    Fieldset for application settings.
    """
    
    label = _(u'Application')
    fields = field.Fields(IFacebookSettings).select('app_id')
    
class PostToPageGroup(group.Group):
    """
    Fieldset for post-to-page settings.
    """

    label = _(u'Post to Page')
    fields = field.Fields(IFacebookSettings).select('post_to_page_available',
        'page_id')
    fields['post_to_page_available'].widgetFactory = SingleCheckBoxFieldWidget
    
class LikeButtonGroup(group.Group):
    """
    Fieldset for Like button settings.
    """
    
    label = _(u'Like Button')
    fields = field.Fields(IFacebookSettings).select('like_button_available',
        'like_button_types', 'like_button_layout', 'like_button_show_faces', 
        'like_button_width', 'like_button_action', 'like_button_font', 
        'like_button_color_scheme')
    fields['like_button_available'].widgetFactory = SingleCheckBoxFieldWidget
    fields['like_button_types'].widgetFactory = CheckBoxFieldWidget
    fields['like_button_show_faces'].widgetFactory = SingleCheckBoxFieldWidget

class FacebookSettingsForm(group.GroupForm, form.EditForm):
    """
    Form for the campaign configlet.
    """
    
    label = _(u'Facebook Configuration')
    groups = (ApplicationGroup, PostToPageGroup, LikeButtonGroup,)

class FacebookSettings(FormWrapper):
    
    implements(IFacebookSettingsForm)
    
    index = ViewPageTemplateFile('configlet.pt')
    form = FacebookSettingsForm
