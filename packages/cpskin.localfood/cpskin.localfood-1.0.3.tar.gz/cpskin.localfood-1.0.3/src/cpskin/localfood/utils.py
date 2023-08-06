# -*- coding: utf-8 -*-

from datetime import datetime
from plone.formwidget.datetime.z3cform.widget import DateWidget


def check_widget_value(widget):
    """ Verify if the value of the given widget is empty or not """
    if isinstance(widget, DateWidget):
        if widget.value is None or len(widget.value) != 3:
            return False
        return (widget.value[0] != '' and widget.value[1] != '' and
                widget.value[2] != '')
    return widget.value and True or False


def format_widget_value(widget):
    """ Return the formatted value for a given widget """
    if isinstance(widget, DateWidget):
        return datetime(*widget.value).strftime('%d/%m/%Y')
    return widget.value
