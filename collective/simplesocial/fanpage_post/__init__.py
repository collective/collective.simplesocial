from Products.CMFCore.permissions import setDefaultRoles

def initialize(context):
    setDefaultRoles('simplesocial: Post to fan page', ['Manager'])
