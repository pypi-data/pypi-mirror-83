# -*- coding: utf-8 -*-
from imio.gdpr import DEFAULT_GDPR_FILES
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DefaultPage(BrowserView):

    index = ViewPageTemplateFile('default_gdpr_text.pt')


class GDPRView(BrowserView):

    index = ViewPageTemplateFile('gdpr_view.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        nav_root = api.portal.get_navigation_root(self.context)
        for filename in DEFAULT_GDPR_FILES:
            gdpr_file = getattr(nav_root, filename, None)
            if gdpr_file and gdpr_file.Language() == self.context.Language():  # noqa
                return self.request.response.redirect(gdpr_file.absolute_url())
        return self.index()

    def content(self):
        text = api.portal.get_registry_record(
            'imio.gdpr.interfaces.IGDPRSettings.text',
            default='',
        )
        return text
