# -*- coding: utf-8 -*-
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from cpskin.localfood import _
from cpskin.localfood import utils


class ICommunityGarden(model.Schema):
    """ Marker interface and Dexterity Python Schema for CommunityGarden
    """

    owner = schema.TextLine(
        title=_('Owner'),
        required=False,
    )

    project_author = schema.TextLine(
        title=_('Project Author'),
        required=False,
    )

    manager = schema.TextLine(
        title=_('Manager'),
        required=False,
    )

    inauguration = schema.TextLine(
        title=_('Inauguration'),
        required=False,
    )

    gardener = schema.TextLine(
        title=_('Gardener'),
        required=False,
    )

    address = schema.TextLine(
        title=_('Address'),
        required=False,
    )

    image = NamedBlobImage(
        title=_('Lead image'),
        required=False,
    )


@implementer(ICommunityGarden)
class CommunityGarden(Container):
    """
    """


class CommunityGardenView(view.DefaultView):

    _cards_fields = (
        'owner',
        'project_author',
        'manager',
        'inauguration',
        'gardener',
        'address',
    )

    @property
    def filtered_widgets(self):
        """
        Return a list of dictionary with widgets label and values
        """
        return [
            {'label': w.label, 'value': utils.format_widget_value(w)}
            for w in self.widgets.values()
            if (w.__name__ in self._cards_fields and
                utils.check_widget_value(w) is True)
        ]

    @property
    def documents(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type": "File"},
        )

    @property
    def images(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type": "Image"},
        )
