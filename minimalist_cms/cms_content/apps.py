from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CMSContentConfig(AppConfig):

    name = 'minimalist_cms.cms_content'
    verbose_name = _('Minimalist content modules')
