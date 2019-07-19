from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import get_language, ugettext_lazy as _

from minimalist_cms.cms_content.models.fields import ContainerField


class PageManager(models.Manager):

    def get_initial_position(self, page):
        # TODO implement
        if not page.position:
            return 1
        return page.position


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
    level = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Level'),
    )
    is_home = models.BooleanField(
        default=False,
    )

    container_header = ContainerField(
        container_name='page_header',
    )

    container_body = ContainerField(
        container_name='page_body',
    )

    class Meta:
        # TODO implement position
        ordering = ['position', 'pk']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __str__(self):
        name = self.get_translation_name()
        if not name:
            name = 'Page {}'.format(self.pk)
        return name

    def save(self, **kwargs):
        self.position = Page.objects.get_initial_position(self)
        if self.parent_page:
            self.level = self.parent_page.level + 1
        else:
            self.level = 0
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

    def get_translation_name(self, language=None):
        translation = self.get_translation(language)
        if translation:
            return translation.name
    get_translation_name.short_description = _('Name')

    def get_translation_path(self, language=None):
        translation = self.get_translation(language)
        if translation:
            return translation.path
    get_translation_path.short_description = _('Path')

    def get_parent_page_for_changelist(self):
        return '{}'.format(self.parent_page or '---')
    get_parent_page_for_changelist.short_description = _('Parent')

    def get_container_admin_name(self, field=None):
        if field:
            return '<b>{}</b>: {} element(s)'.format(
                field.name,
                field.elements.count()
            )
        return ''

    def get_container_admin_names(self):
        names = []
        if self.container_header:
            names.append(self.get_container_admin_name(self.container_header))
        if self.container_body:
            names.append(self.get_container_admin_name(self.container_body))
        if names:
            return mark_safe(', <br>'.join(names))
        return '0'
    get_container_admin_names.short_description = _('Content containers')


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

    @property
    def site(self):
        if self.page:
            return self.page.site

    @property
    def parent_page(self):
        if self.page:
            return self.page.parent_page

    @property
    def position(self):
        if self.page:
            return self.page.position

    @property
    def is_home(self):
        if self.page:
            return self.page.is_home

    @property
    def is_deleted(self):
        if self.page:
            return self.page.is_deleted
