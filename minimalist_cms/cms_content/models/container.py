from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Container(models.Model):

    name = models.SlugField(
        max_length=100,
        verbose_name=_('Name'),
    )

    # generic relation to containerfield object
    # we must be able to handle null
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Object ID'),
    )
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('Content type'),
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta:
        verbose_name = _('Container')
        verbose_name_plural = _('Container')

    def __str__(self):
        if self.content_object:
            return '{} ({}) - {}'.format(
                self.content_object,
                self.content_type,
                self.name,

            )
        return '{} {}'.format(self.name, self.pk)

    def save(self, **kwargs):
        element_qs = self.element_set.all()
        if element_qs:
            element_qs.update(
                object_id=self.object_id,
                content_type=self.content_type,
            )
        super().save(**kwargs)

    def render(self):
        element_qs = self.element_set.all()
        return element_qs

    @property
    def elements(self):
        return self.element_set.all()
