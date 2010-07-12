from plone.i18n.normalizer.base import mapUnicode
import datetime

UNICODE_MAP = {
    8220: '"', 
    8221: '"',
    8216: "'",
    8217: "'",
    2012: "-",
    2013: "-",
    2014: "--",
    2015: "--",
    2019: "'",
}

class js_literal(str):
    """
    Marks a Python string object as a literal so that it is not enclosed
    in quotes when it is passed through js_value.
    """

def js_value(value):
    """
    Given a python value, return the corresponding javascript value.
    """
    
    # A javascript literal
    if type(value) is js_literal:
        return value
    # A date
    if type(value) is datetime.date:
        return 'new Date(%i, %i, %i)' % (value.year, value.month, value.day)
    # A boolean
    if type(value) is bool:
        return str(value).lower()
    # A string
    if type(value) in (str, unicode):
        if not type(value) == unicode:
            value = unicode(value, 'utf-8')
        value = mapUnicode(value, UNICODE_MAP)
        return '"%s"' % (value.replace('"', '\\"').replace("'", "\\'"))
    # A number
    return str(value)

def json_serialize(parent):
    """
    Given a Python list, tuple or dictionary, return the corresponding
    json object.
    """
    
    json_parts = []
    if type(parent) in [list, tuple]:
        for child in parent:
            json_parts.append(json_serialize(child))
        return js_literal('[%s]' % ', '.join(json_parts))
    if type(parent) is dict:
        for (key, value) in parent.items():
            json_parts.append('%s: %s' % (json_serialize(key), json_serialize(value)))
        return js_literal('{%s}' % ', '.join(json_parts))
    return js_value(parent)
    
def json_escape(s):
    return s.replace('"', '\\"').replace("'", "\\'")