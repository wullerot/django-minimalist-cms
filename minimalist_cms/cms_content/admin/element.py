from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from ..models import Element


class ElementAdminForm(forms.ModelForm):

    class Meta:
        model = Element
        fields = '__all__'
        widgets = {}


class ElementAdmin(admin.ModelAdmin):
    """
    Element Admin: only for dev and testing
    """
    form = ElementAdminForm
