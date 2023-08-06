# -*- coding: utf-8 -*-
from imio.gdpr import get_default_text
from imio.gdpr.interfaces import IGDPRSettings
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def udpate_default_template(context):
    text = get_default_text(api.portal.get())
    api.portal.set_registry_record('text', text, interface=IGDPRSettings)


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-imio.gdpr:default',
    )
