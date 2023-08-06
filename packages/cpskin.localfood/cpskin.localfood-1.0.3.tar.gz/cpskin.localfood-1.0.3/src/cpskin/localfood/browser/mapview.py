# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from collective.geo.json.browser.jsonview import JsonFolderDocument
from collective.geo.leaflet.interfaces import IGeoMap
from plone import api


class MapView(BrowserView):

    @property
    def json(self):
        brains = api.content.find(
            context=self.context,
        )
        json_view = MapViewJSON(self.context, self.request)
        json_view.set_brains(brains)
        return json_view.get_json()

    @property
    def geomap(self):
        return IGeoMap(self.context)


class MapViewJSON(JsonFolderDocument):

    def set_brains(self, brains):
        self.brains = brains

    def get_brains(self):
        """Needed by get_json method from collective.geo.json."""
        return self.brains
