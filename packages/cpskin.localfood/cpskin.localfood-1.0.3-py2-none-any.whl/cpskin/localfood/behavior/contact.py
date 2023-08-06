# -*- coding: utf-8 -*-

from cpskin.core.behaviors import directorycontact
from collective.contact.core import _ as CCMF
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from cpskin.localfood import _


@provider(IFormFieldProvider)
class IContactCard(directorycontact.IDirectoryContactDetails):

    form.omitted('use_parent_address')
    form.omitted('street')
    form.omitted('number')
    form.omitted('additional_address_details')
    form.omitted('zip_code')
    form.omitted('city')
    form.omitted('region')
    form.omitted('country')
    form.omitted('im_handle')

    model.fieldset(
        'address',
        label=CCMF(u'Address'),
        fields=['lastname', 'firstname', 'organization', 'contact_address'],
    )

    lastname = schema.TextLine(
        title=_(u'Lastname'),
        required=False,
    )

    firstname = schema.TextLine(
        title=_(u'Firstname'),
        required=False,
    )

    organization = schema.TextLine(
        title=_(u'Organization'),
        required=False,
    )

    contact_address = schema.TextLine(
        title=_('Address'),
        required=False,
    )


@implementer(IContactCard)
@adapter(IDexterityContent)
class ContactCard(object):

    def __init__(self, context):
        self.context = context
