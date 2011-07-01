from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from collective.simplesocial.browser.interfaces import IFacebookSettingsForm
from collective.simplesocial import json

JAVASCRIPT = """
  SimpleSocial.addSettings(%(settings)s);
  window.fbAsyncInit = function() {
    if (navigator.appVersion.indexOf('MSIE') != -1) {
        version = parseFloat(navigator.appVersion.split('MSIE')[1]);
        if (version <= 6) return;
    }
    SimpleSocial.connect(function(response) {
        if (response.connected) {
            SimpleSocial.processQueue();
        }
    });
  };
  (function() {
    var e = document.createElement('script'); e.async = true;
    e.src = document.location.protocol +
      '//connect.facebook.net/en_US/all.js';
    document.getElementById('fb-root').appendChild(e);
  }());
"""

class FBInitViewlet(ViewletBase):
    index = ViewPageTemplateFile('fb_init.pt')
    init_options = ''

    def available(self):
        """
        Check to see whether we should perform the normal initialization
        sequence.
        """
        
        if IFacebookSettingsForm.providedBy(self.view):
            # This is the settings form, so all bets are off.
            return False
        settings = self._getSettings()
        if 'app_id' in settings.keys():
            try:
                int(settings['app_id'])
                return True
            except ValueError:
                # This is not a valid application ID.
                return False
        return False

    def update(self):
        super(FBInitViewlet, self).update()
        self.jscript = JAVASCRIPT % dict(
                settings=json.dumps(self._getSettings()))
        
    def _getSettings(self):
        """
        Returns a Python dictionary containing the initialization options
        to be used when loading the Facebook API.
        """
        
        pprops = getToolByName(self.context, 'portal_properties')
        fb_properties = pprops.get('fb_properties', None)
        items = fb_properties.propertyItems()
        return dict([prop for prop in items \
            if not prop[0] == 'title' and not prop[1] == ''])
