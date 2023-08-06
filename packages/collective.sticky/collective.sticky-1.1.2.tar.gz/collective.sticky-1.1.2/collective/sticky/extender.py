from zope.interface import implements
from zope.component import adapts
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from plone.indexer import indexer
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces import IATNewsItem, IATEvent

from collective.sticky import _
from collective.sticky.interfaces import IBrowserLayer


class CheckboxField(ExtensionField, atapi.BooleanField):
    pass


class StickyBaseSchemaExtender(object):
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IBrowserLayer

    def __init__(self, context):
        pass

    _fields = [CheckboxField('sticky',
        schemata='categorization',
        widget=atapi.BooleanWidget(
            label=_('Should this page be "sticky" and appear at the top of sticky-aware collections?'),
            ),
        default=False,
        )]

    def getFields(self):
        return self._fields


class StickyNewsSchemaExtender(StickyBaseSchemaExtender):
    adapts(IATNewsItem)


@indexer(IATNewsItem)
def sticky_sort_news(context):
    date = context.getField('effectiveDate').get(context)
    if date is None:
        date = context.getField('creation_date').get(context)
    return (context.getField('sticky').get(context), date.timeTime())


@indexer(IATNewsItem)
def is_sticky_news(context):
    return context.getField('sticky').get(context)


class StickyEventSchemaExtender(StickyBaseSchemaExtender):
    adapts(IATEvent)


@indexer(IATEvent)
def sticky_sort_event(context):
    date = context.getField('startDate').get(context)
    return (context.getField('sticky').get(context), date.timeTime())


@indexer(IATEvent)
def is_sticky_event(context):
    return context.getField('sticky').get(context)
