from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..container import Container


class ContainerField(models.ForeignKey):

    description = _('Minimalist CMS conntent container field')

    def __init__(self, *args, **kwargs):
        self.container_name = kwargs.pop('container_name')
        to = kwargs.pop('to', 'cms_content.Container')
        on_delete = kwargs.pop('on_delete', models.CASCADE)
        kwargs['blank'] = False
        kwargs['null'] = True
        kwargs['editable'] = False
        kwargs['related_name'] = self.container_name
        kwargs['limit_choices_to'] = {'name': self.container_name}
        super(ContainerField, self).__init__(to, on_delete, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(ContainerField, self).deconstruct()
        # Add the container name to the
        kwargs['container_name'] = self.container_name
        return name, path, args, kwargs

    def _get_new_container(self, model_instance):
        """
        Create a new container
        """
        return Container.objects.create(
            name=self.name,
            content_object=model_instance,
        )

    def pre_save(self, model_instance, add):
        """
        Return field's value just before saving.
        Create a container if we have none or one with a wrong name
        """
        container = getattr(model_instance, self.name, None)
        container_name = getattr(container, 'name', '')
        if not container_name == self.container_name:
            setattr(
                model_instance,
                self.name,
                self._get_new_container(model_instance)
            )
            container = getattr(model_instance, self.name)
        if not getattr(container, 'content_object', None) == model_instance:
            container.content_object = model_instance
        return super(ContainerField, self).pre_save(model_instance, add)
