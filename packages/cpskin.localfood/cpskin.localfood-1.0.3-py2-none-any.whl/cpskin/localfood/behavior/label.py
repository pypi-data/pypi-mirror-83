# -*- coding: utf-8 -*-

from collective.z3cform.keywordwidget.field import Keywords
from cpskin.locales import CPSkinMessageFactory as CPMF
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from zope.interface import provider

from cpskin.localfood import _


@provider(IFormFieldProvider)
class ILabels(model.Schema):
    model.fieldset(
        'categorization',
        label=CPMF(u'label_schema_categorization', default=u'Categorization'),
        fields=['labels'],
    )

    form.widget(labels='collective.z3cform.keywordwidget.widget.KeywordFieldWidget')  # noqa
    labels = Keywords(
        title=_(u'Labels'),
        description=_(u'Labels displayed under the content body'),
        required=False,
        # Automatically get the index in catalog by name
        index_name='labels',
    )
