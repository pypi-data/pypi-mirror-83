# -*- coding: utf-8 -*-

from Acquisition import aq_base
from plone.app.layout.viewlets import common as base


class LabelsViewlet(base.ViewletBase):

    @property
    def can_view(self):
        labels = getattr(aq_base(self.context), 'labels', None)
        if labels:
            return True
        return False
