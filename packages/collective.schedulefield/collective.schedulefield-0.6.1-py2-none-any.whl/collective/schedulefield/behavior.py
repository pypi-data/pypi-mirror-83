# -*- coding: utf-8 -*-
"""
collective.schedulefield
------------------------

Created by mpeeters
:license: GPL, see LICENCE.txt for more details.
"""

from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.view import WidgetsView
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel.directives import fieldset
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider

from collective.schedulefield import _
from collective.schedulefield.schedule import Schedule


@provider(IFormFieldProvider)
class IScheduledContent(Interface):

    fieldset(
        'schedule',
        label=_('Schedule'),
        fields=['schedule', 'test'],
    )

    schedule = Schedule(
        title=_(u'Schedule'),
        required=False,
    )


@implementer(IScheduledContent)
@adapter(IDexterityContent)
class ScheduledContent(object):

    def __init__(self, context):
        self.context = context


class WidgetView(WidgetsView):
    schema = IScheduledContent
