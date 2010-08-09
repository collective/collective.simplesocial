from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.portlets.interfaces import IPortletType
from collective.simplesocial import simplesocialMessageFactory as _

def null_upgrade_step(setup_tool):
    """
    This is a null upgrade, use it when nothing happens
    """
    pass
    
def fbconnect_10_to_14(setup_tool):
    """
    Updates the installed profiles to reflect new configuration defaults.
    """
        
    profile_id = 'profile-collective.simplesocial:fbconnect'
    setup_tool.runImportStepFromProfile(profile_id, 'controlpanel')
    setup_tool.runImportStepFromProfile(profile_id, 'jsregistry')
    setup_tool.runImportStepFromProfile(profile_id, 'propertiestool')
    
    jsregistry = getToolByName(setup_tool, 'portal_javascripts')
    fanpage_post_id = '++resource++simplesocial_fanpage_post.js'
    if fanpage_post_id in jsregistry.getResourceIds():
        jsregistry.moveResourceAfter(fanpage_post_id, '++resource++simplesocial.js')
    
def fanbox_10_to_14(setup_tool):
    """
    Updates the installed profiles to reflect new configuration defaults.
    """
    
    # If the fbconnect profile isn't already installed, install it.
    fbconnect_profile = 'profile-collective.simplesocial:fbconnect'
    if not setup_tool.getProfileImportDate(fbconnect_profile):
        setup_tool.runAllImportStepsFromProfile(fbconnect_profile)
        IStatusMessage(setup_tool.REQUEST).addStatusMessage(
            _(u'The Facebook Like Box portlet now requires a Facebook application.' +
            ' Please visit the Facebook Settings control panel to configure one.')
        )

    portlet_name = 'collective.simplesocial.fanbox.FacebookFanBox'
    portlet = getUtility(IPortletType, name=portlet_name)
    portlet.title = 'Facebook Like Box'

def fanpage_post_10_to_14(setup_tool):
    """
    Updates the installed profiles to reflect new configuration defaults.
    """
    
    jsregistry = getToolByName(setup_tool, 'portal_javascripts')
    old_id = 'simplesocial_fanpage_post.js'
    new_id = '++resource++simplesocial_fanpage_post.js'
    jsregistry.renameResource(old_id, new_id)
    if '++resource++simplesocial.js' in jsregistry.getResourceIds():
        jsregistry.moveResourceAfter(new_id, '++resource++simplesocial.js')