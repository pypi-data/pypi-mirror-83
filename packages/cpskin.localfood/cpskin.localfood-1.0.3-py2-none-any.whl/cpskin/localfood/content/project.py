# -*- coding: utf-8 -*-
from plone.dexterity.browser import view
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from cpskin.localfood import _
from cpskin.localfood import utils


class IProject(model.Schema):
    """ Marker interface and Dexterity Python Schema for Project
    """

    area = schema.Text(
        title=_('Area'),
        required=True,
    )

    owner = schema.TextLine(
        title=_('Owner'),
        required=True,
    )

    occupant = schema.Text(
        title=_('Occupant'),
        required=False,
    )

    availability = schema.Text(
        title=_('Availability'),
        required=False,
    )

    occupationStart = schema.Date(
        title=_('Start of occupation'),
        required=False,
    )

    cultivationType = schema.Text(
        title=_('Type of cultivation'),
        required=False,
    )

    orientation = schema.Text(
        title=_('Orientation'),
        required=False,
    )

    accessibility = schema.Text(
        title=_('Accessibility'),
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


@implementer(IProject)
class Project(Container):
    """
    """


class ProjectView(view.DefaultView):

    _cards_fields = (
        'area',
        'owner',
        'occupant',
        'availability',
        'occupationStart',
        'cultivationType',
        'orientation',
        'accessibility',
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
