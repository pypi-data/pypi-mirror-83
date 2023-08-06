# -*- coding: utf-8 -*-
from plone import api
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.interfaces import IDexteritySchema
from plone.namedfile.interfaces import INamedBlobFileField
from plone.namedfile.interfaces import INamedImageField
from z3c.caching.interfaces import IPurgePaths
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.schema import getFieldsInOrder

import six


@implementer(IPurgePaths)
@adapter(IDexteritySchema)
class ScalesPurgePaths(object):
    """Paths to purge for Dexterity object fields
    """
    def __init__(self, context):
        self.context = context

    def getScales(self):
        scale_util = api.content.get_view(
            'images',
            self.context,
            self.context.REQUEST)
        return scale_util.getAvailableSizes().keys()

        # registry = getUtility(IRegistry)
        # reg_list = registry['plone.allowed_sizes']
        # sizes = [i.split(' ', 1)[0] for i in reg_list]
        # sizes.append('download')
        # return sizes

    def getRelativePaths(self):
        prefix = '/' + self.context.virtual_url_path()

        def fieldFilter():
            portal_type = self.context.getPortalTypeName()
            fti = getUtility(IDexterityFTI, name=portal_type)
            schema = fti.lookupSchema()
            fields = getFieldsInOrder(schema)
            assignable = IBehaviorAssignable(self.context, None)
            for behavior in assignable.enumerateBehaviors():
                if behavior.marker:
                    new_fields = getFieldsInOrder(behavior.marker)
                    if len(new_fields) > 0:
                        fields = fields + new_fields

            obj_fields = []
            for key, value in fields:
                is_image = INamedImageField.providedBy(value)
                is_file = INamedBlobFileField.providedBy(value)
                if is_image or is_file:
                    obj_fields.append(value)
            return obj_fields

        for item in fieldFilter():
            field = item.getName()
            value = item.get(self.context)
            if not value:
                continue

            if INamedImageField.providedBy(item):
                for size in self.getScales():
                    yield '{0}/@@images/{1}/{2}'.format(prefix, field, size,)
                    yield '{0}/@@download/{1}'.format(prefix, field)
            else:
                filename = value.filename
                if six.PY2 and isinstance(filename, six.text_type):
                    filename = filename.encode('utf-8')
                yield '{0}/view/{1}.{2}/@@download/{3}'.format(
                    prefix, '++widget++form.widgets', field, filename)
                yield '{0}/@@download/{1}/{2}'.format(prefix, field, filename)

    def getAbsolutePaths(self):
        return []
