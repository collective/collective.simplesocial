from zope.component import adapts
from zope.interface import implements
from z3c.form import form, field, group
from z3c.form.browser.checkbox import CheckBoxFieldWidget, \
    SingleCheckBoxFieldWidget
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from collective.simplesocial.browser.interfaces import IFacebookSettingsForm, \
    IFacebookSettings
from collective.simplesocial import simplesocialMessageFactory as _

class PropertySheetProperty(object):
    """
    Gets and sets a value on a property sheet based on a schema field.
    """
    
    def __init__(self, field, prop_type):
        self._field = field
        self._prop_type = prop_type
        
    def __get__(self, instance, owner):
        return instance.context.getProperty(self._field.__name__,
            getattr(self._field, 'default', None))
        
    def __set__(self, instance, value):
        if self._prop_type == 'string' and value is None:
            value = u''
        if instance.context.hasProperty(self._field.__name__):
            instance.context.manage_changeProperties(**{self._field.__name__: value})
        else:
            instance.context.manage_addProperty(self._field.__name__, value,
                self._prop_type)

class FacebookSettingsAdapter(object):
    implements(IFacebookSettings)
    adapts(ISiteRoot)
    
    def __init__(self, context):
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.fb_properties
        self.encoding = pprop.site_properties.default_charset
        
    app_id = PropertySheetProperty(IFacebookSettings['app_id'], 'string')
    post_to_page_available = PropertySheetProperty(IFacebookSettings['post_to_page_available'], 'boolean')
    page_id = PropertySheetProperty(IFacebookSettings['page_id'], 'string')
    like_button_available = PropertySheetProperty(IFacebookSettings['like_button_available'], 'boolean')
    like_button_types = PropertySheetProperty(IFacebookSettings['like_button_types'], 'lines')
    like_button_layout = PropertySheetProperty(IFacebookSettings['like_button_layout'], 'string')
    like_button_show_faces = PropertySheetProperty(IFacebookSettings['like_button_show_faces'], 'boolean')
    like_button_width = PropertySheetProperty(IFacebookSettings['like_button_width'], 'int')
    like_button_action = PropertySheetProperty(IFacebookSettings['like_button_action'], 'string')
    like_button_font = PropertySheetProperty(IFacebookSettings['like_button_font'], 'string')
    like_button_color_scheme = PropertySheetProperty(IFacebookSettings['like_button_color_scheme'], 'string')
    like_button_ref = PropertySheetProperty(IFacebookSettings['like_button_ref'], 'string')

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
        'like_button_color_scheme', 'like_button_ref')
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
