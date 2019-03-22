from __future__ import unicode_literals

from django.contrib import admin

from .models import TestModel


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    pass
