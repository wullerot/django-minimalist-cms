from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Element(models.Model):

    # explicit relation to the placeholder
    container = models.ForeignKey(
        'cms_content.Container',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        verbose_name=_('Container'),
    )

    # generic relation to containerfield object
    # we must be able to handle null
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Content type'),
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Object ID'),
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    # element attrs
    position = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Position'),
    )
    parent_element = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='element_set',
        verbose_name=_('Parent element'),
    )
    element_type = models.SlugField(
        max_length=100,
        verbose_name=_('Type'),
    )

    class Meta:
        ordering = [
            'position',
        ]
        verbose_name = _('Element')
        verbose_name_plural = _('Element')

    def __str__(self):
        return 'Minimalist Conatiner {}'.format(self.pk)

    def save(self, **kwargs):
        container_parent = getattr(self.container, 'content_object', None)
        if container_parent:
            self.content_object = container_parent
        super().save(**kwargs)
