from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TestModel(models.Model):
    name = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return '{}'.format(self.name)
