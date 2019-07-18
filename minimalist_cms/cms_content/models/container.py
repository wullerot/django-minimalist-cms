from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Container(models.Model):

    name = models.SlugField(
        max_length=100,
        verbose_name=_('Name'),
    )

    class Meta:
        verbose_name = _('Container')
        verbose_name_plural = _('Container')

    def __str__(self):
        return '{} {}'.format(self.name, self.pk)
