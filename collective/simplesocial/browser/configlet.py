from zope.component import adapts
from zope.interface import implements
from z3c.form import form, field
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
        
    app_id = ProxyFieldProperty(IFacebookSettings['app_id'])
    page_id = ProxyFieldProperty(IFacebookSettings['page_id'])

class FacebookSettingsForm(form.EditForm):
    """
    Form for the campaign configlet.
    """
    
    label = _(u'Facebook Configuration')
    fields = field.Fields(IFacebookSettings)

class FacebookSettings(FormWrapper):
    
    implements(IFacebookSettingsForm)
    
    index = ViewPageTemplateFile('configlet.pt')
    form = FacebookSettingsForm

