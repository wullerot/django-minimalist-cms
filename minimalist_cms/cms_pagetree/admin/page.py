from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin

from ..models import Page, PageTranslation


class PageTranslationInlineForm(forms.ModelForm):

    class Meta:
        model = PageTranslation
        fields = '__all__'
        widgets = {
            'language': forms.Select(
                choices=settings.LANGUAGES,
            )
        }


class PageTranslationInline(admin.StackedInline):

    form = PageTranslationInlineForm
    model = PageTranslation
    extra = len(settings.LANGUAGES)
    min_num = len(settings.LANGUAGES)
    max_num = len(settings.LANGUAGES)


class PageAdminForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = '__all__'
        widgets = {}


class PageAdmin(admin.ModelAdmin):

    form = PageAdminForm
    list_display = [
        'get_translation_name',
        'get_translation_path',
        'position',
    ]
    inlines = [
        PageTranslationInline,
    ]
