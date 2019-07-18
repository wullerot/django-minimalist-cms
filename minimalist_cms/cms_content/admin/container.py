from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from ..models import Container


class ContainerAdminForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = '__all__'
        widgets = {}


class ContainerAdmin(admin.ModelAdmin):

    form = ContainerAdminForm
