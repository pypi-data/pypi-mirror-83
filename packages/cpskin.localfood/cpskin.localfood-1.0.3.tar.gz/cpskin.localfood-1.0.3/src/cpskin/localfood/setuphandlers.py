# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName


def installLocalfood(context):
    site = context.getSite()
    groups_tool = site.portal_groups
    portal_memberdata = getToolByName(site, "portal_memberdata")

    for group_id in ('local_producer', 'horeca_business'):
        if group_id not in groups_tool.getGroupIds():
            groups_tool.addGroup(group_id)

    properties = (
        ('producer_name', 'string', ''),
        ('producer_address', 'text', ''),
        ('producer_phone_number', 'string', ''),
        ('producer_mobile', 'string', ''),
        ('producer_email', 'string', ''),
        ('producer_company_number', 'string', ''),
        ('proposed_products', 'lines', []),
        ('localfood_chart_acceptation', 'boolean', False),
        ('genuine_form_data_and_quality', 'boolean', False),
        ('business_name', 'string', ''),
        ('purchasing_manager', 'string', ''),
        ('horeca_address', 'text', ''),
        ('horeca_phone_number', 'string', ''),
        ('horeca_mobile', 'string', ''),
        ('horeca_email', 'string', ''),
        ('horeca_company_number', 'string', ''),
        ('wanted_products', 'lines', []),
        ('genuine_form_data', 'boolean', False),
    )
    for property_id, value_type, default_value in properties:
        property_id = 'localfood_{0}'.format(property_id)
        if not portal_memberdata.hasProperty(property_id):
            portal_memberdata.manage_addProperty(
                id=property_id,
                type=value_type,
                value=default_value,
            )


def uninstallLocalfood(context):
    pass


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'cpskin.localfood:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
