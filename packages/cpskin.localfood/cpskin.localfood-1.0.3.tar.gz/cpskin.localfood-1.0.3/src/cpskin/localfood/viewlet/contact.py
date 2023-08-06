# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common as base
from cpskin.locales import CPSkinMessageFactory as CPMF
from collective.contact.core import _ as CCMF

import collections

from cpskin.localfood import _


class ContactCardViewlet(base.ViewletBase):

    # XXX Should be improved to by more dynamic
    _fields = (
        (_(u'Lastname'), 'lastname'),
        (_(u'Firstname'), 'firstname'),
        (_(u'Organization'), 'organization'),
        (_(u'Address'), 'contact_address'),
        (CPMF('Phones'), 'phone'),
        (CCMF('Cell phone'), 'cell_phone'),
        (CCMF(u'Fax'), 'fax'),
        (CCMF(u'Email'), 'email'),
        (CCMF(u'Website'), 'website'),
    )

    @property
    def can_view(self):
        return len(self.widgets) > 0

    @property
    def widgets(self):
        """ Return a list of dictionary with widgets label and values """
        return [
            {'label': k, 'value': self.format_value(v)}
            for k, v in self._fields
            if self.has_value(v)
        ]

    def has_value(self, key):
        if self.get_value(key):
            return True
        return False

    def get_value(self, key):
        return getattr(self.context, key, None)

    def format_value(self, key, separator=u', '):
        value = self.get_value(key)
        if isinstance(value, basestring):
            return value
        if isinstance(value, collections.Iterable):
            return separator.join(value)
        return value
