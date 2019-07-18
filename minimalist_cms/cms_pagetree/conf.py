from __future__ import unicode_literals

from django.conf import settings


PAGE_TEMPLATES = getattr(
    settings,
    'CMS_PAGETREE_PAGE_TEMPLATES',
    [
        ('cms_pagetree/page/default.html', 'default'),
    ]
)
