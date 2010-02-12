from plone.i18n.normalizer.base import mapUnicode

UNICODE_MAP = {
    8220: '"', 
    8221: '"',
    8216: "'",
    8217: "'",
    2012: "-",
    2013: "-",
    2014: "--",
    2015: "--",
}

def json_escape(s):
    return s.replace('"', '\\"').replace("'", "\\'")

def json_serialize(parent):
    """
    Given a Python list, tuple or dictionary, return the corresponding
    json object.
    """
    json_parts = []
    if type(parent) in [list, tuple]:
        for child in parent:
            json_parts.append(json_serialize(child))
        return '[%s]' % ', '.join(json_parts)
    if type(parent) is dict:
        for (key, value) in parent.items():
            json_parts.append('%s: %s' % (json_serialize(key), json_serialize(value)))
        return '{%s}' % ', '.join(json_parts)
    return '"%s"' % json_escape(mapUnicode(parent, UNICODE_MAP))