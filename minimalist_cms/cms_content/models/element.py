from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Element(models.Model):

    container = models.ForeignKey(
        'cms_content.Container',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name=_('Container'),
    )
    position = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Position'),
    )
    parent_element = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
        related_name='element_set',
        verbose_name=_('Parent element'),
    )
    element_type = models.SlugField(
        max_length=100,
        verbose_name=_('Type'),
    )

    class Meta:
        ordering = [
            'container',
            'parent_element',
            'position',
        ]
        verbose_name = _('Container')
        verbose_name_plural = _('Container')

    def __str__(self):
        return 'Minimalist Conatiner {}'.format(self.pk)
