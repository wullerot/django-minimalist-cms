from __future__ import unicode_literals

from django.contrib import admin

from .page import Page, PageAdmin


admin.site.register(Page, PageAdmin)
