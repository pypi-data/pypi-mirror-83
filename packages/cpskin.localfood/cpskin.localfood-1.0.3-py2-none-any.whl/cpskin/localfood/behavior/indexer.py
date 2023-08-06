# -*- coding: utf-8 -*-

from cpskin.core import indexer


class LabelsIndexer(indexer.BaseTagIndexer):

    def __call__(self):
        return self._getFieldContent('labels')
