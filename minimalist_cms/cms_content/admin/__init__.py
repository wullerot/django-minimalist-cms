from __future__ import unicode_literals

from django.contrib import admin

from .container import Container, ContainerAdmin


admin.site.register(Container, ContainerAdmin)
