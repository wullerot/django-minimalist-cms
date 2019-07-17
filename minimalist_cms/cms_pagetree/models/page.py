from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import get_language, ugettext_lazy as _


class PageManager(models.Manager):

    def get_initial_position(self, page):
        # TODO implement
        position = 1
        return position


@python_2_unicode_compatible
class Page(models.Model):

    objects = PageManager()

    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    date_modified = models.DateTimeField(
        auto_now=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    site = models.ForeignKey(
        'sites.Site',
        default=settings.SITE_ID,
        on_delete=models.CASCADE,
        verbose_name=_('Site'),
    )
    parent_page = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        related_name='pages_set',
        verbose_name=_('Parent page')
    )
    position = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Position'),
    )
    is_home = models.BooleanField(
        default=False,
    )

    class Meta:
        # TODO implement position
        ordering = ['position', 'pk']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __str__(self):
        return 'Page {}'.format(self.pk)

    def save(self, **kwargs):
        self.position = Page.objects.get_initial_position(self)
        super(Page, self).save(**kwargs)
        if self.pk:
            for translation in self.translation_set.all():
                translation.save()

    def get_translation(self, language=None):
        # TODO find a less naive way to do this
        language = language or get_language()
        try:
            translation = self.translation_set.get(language=language)
            return translation
        except Exception:
            pass

    def get_translation_path(self, language=None):
        translation = self.get_translation(language)
        if translation:
            return translation.path
    get_translation_path.short_description = _('Path')

    def get_parent_page_for_changelist(self):
        return '{}'.format(self.parent_page or '---')
    get_parent_page_for_changelist.short_description = _('Parent')


@python_2_unicode_compatible
class PageTranslation(models.Model):

    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    date_modified = models.DateTimeField(
        auto_now=True,
    )

    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='translation_set',
        verbose_name=_('Page'),
    )
    language = models.CharField(
        max_length=8,
        default=get_language(),
        verbose_name=_('Language'),
    )
    name = models.CharField(
        max_length=200,
        default='',
        verbose_name=_('Title'),
    )
    slug = models.SlugField(
        max_length=200,
        default='',
        blank=True,
        verbose_name=_('Slug'),
    )
    path = models.CharField(
        max_length=1000,
        default='',
        editable=False,
    )

    class Meta:
        # TODO get this right
        ordering = ['language']
        unique_together = [
            ['page', 'language'],
        ]
        verbose_name = _('Page translation')
        verbose_name_plural = _('Page translations')

    def __str__(self):
        return '{} {}'.format(self.page, self.language)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.path = self.build_path()
        super(PageTranslation, self).save(**kwargs)

    def build_path(self):
        # TODO find a less naive way to do this
        if self.page.parent_page:
            parent = self.page.parent_page.get_translation(
                language=self.language
            )
            prefix = '{}'.format(parent.build_path())
        else:
            prefix = '/{}/'.format(self.language)
            if self.page.is_home:
                return prefix
        return '{}{}/'.format(prefix, self.slug)
