from __future__ import unicode_literals

from django.contrib import admin

from .container import Container, ContainerAdmin
from .element import Element, ElementAdmin


admin.site.register(Container, ContainerAdmin)
admin.site.register(Element, ElementAdmin)
