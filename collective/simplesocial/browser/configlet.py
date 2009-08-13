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
    
    api_key = schema.TextLine(
        title = _(u'API Key'),
        description = _(u'Enter the API Key for your Facebook application.')
    )

class FacebookSettingsAdapter(object):
    implements(IFacebookSettings)
    adapts(ISiteRoot)
    
    def __init__(self, context):
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.fb_properties
        self.encoding = pprop.site_properties.default_charset

    def get_api_key(self):
        return self.context.getProperty('api_key')
    def set_api_key(self, value):
        if self.context.hasProperty('api_key'):
            self.context._updateProperty('api_key', value)
        else:
            self.context._setProperty('api_key', value)
    api_key = property(get_api_key, set_api_key)

class FacebookSettingsForm(ControlPanelForm):
    template = ViewPageTemplateFile('configlet.pt')
    
    form_fields = form.FormFields(IFacebookSettings)
    form_name = _(u'Facebook Connect Configuration')
