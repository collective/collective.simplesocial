from zope.interface import implements
from zope.component import adapts
from zope.schema.interfaces import ICollection

from plone.app.portlets.exportimport.interfaces import \
    IPortletAssignmentExportImportHandler
from plone.app.portlets.exportimport.portlets import \
    PropertyPortletAssignmentExportImportHandler as base

from collective.simplesocial.fanbox.facebookfanbox import IFacebookFanBox


class PropertyPortletAssignmentExportImportHandler(base):
    """Import portlet assignment settings based on zope.schema properties
    
    This overrides default adapter to properly import Facebook FanBox portlet
    'stream' choice field with integer values from vocabulary.
    """

    implements(IPortletAssignmentExportImportHandler)
    adapts(IFacebookFanBox)

    def import_node(self, interface, child):
        """Import a single <property /> node
        """
        property_name = child.getAttribute('name')

        field = interface.get(property_name, None)
        if field is None:
            return

        field = field.bind(self.assignment)
        value = None

        # If we have a collection, we need to look at the value_type.
        # We look for <element>value</element> child nodes and get the
        # value from there
        if ICollection.providedBy(field):
            value_type = field.value_type
            value = []
            for element in child.childNodes:
                if element.nodeName != 'element':
                    continue
                element_value = self.extract_text(element)
                value.append(self.from_unicode(value_type, element_value))
            value = self.field_typecast(field, value)

        # We need to handle Choice field with integer values separarately here
        elif field.__name__ == 'stream':
            value = int(self.extract_text(child))

        # Otherwise, just get the value of the <property /> node
        else:
            value = self.extract_text(child)
            value = self.from_unicode(field, value)

        field.validate(value)
        field.set(self.assignment, value)
