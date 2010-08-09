from zope.component import adapts
from zope.interface import Interface, implements
from zope import schema
from zope.formlib import form
from plone.app.controlpanel.form import ControlPanelForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from collective.simplesocial import simplesocialMessageFactory as _

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

class FacebookSettingsAdapter(object):
    implements(IFacebookSettings)
    adapts(ISiteRoot)
    
    def __init__(self, context):
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.fb_properties
        self.encoding = pprop.site_properties.default_charset

    def get_app_id(self):
        return self.context.getProperty('app_id')
    def set_app_id(self, value):
        if self.context.hasProperty('app_id'):
            self.context._updateProperty('app_id', value)
        else:
            self.context._setProperty('app_id', value)
    app_id = property(get_app_id, set_app_id)

    def get_page_id(self):
        return self.context.getProperty('page_id')
    def set_page_id(self, value):
        if self.context.hasProperty('page_id'):
            self.context._updateProperty('page_id', value)
        else:
            self.context._setProperty('page_id', value)
    page_id = property(get_page_id, set_page_id)

class FacebookSettingsForm(ControlPanelForm):
    template = ViewPageTemplateFile('configlet.pt')
    form_name = _(u'Facebook Configuration')
    
    @property
    def form_fields(self):
        form_fields = form.FormFields(IFacebookSettings)
        qi = getToolByName(self.context, 'portal_quickinstaller')
        if not qi.isProductInstalled('collective.simplesocial.fanpage_post'):
            form_fields = form_fields.omit('page_id')
        return form_fields
