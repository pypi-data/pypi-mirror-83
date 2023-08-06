# -*- coding: utf-8 -*-
from cpskin.core.browser import folderview
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('cpskin.localfood')

folderview.ADDABLE_TYPES += ['Link']
