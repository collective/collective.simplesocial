"""Main product initializer
"""

try:
    import json
except ImportError:
    import simplejson as json

from zope.i18nmessageid import MessageFactory

# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

simplesocialMessageFactory = MessageFactory('collective.simplesocial')
