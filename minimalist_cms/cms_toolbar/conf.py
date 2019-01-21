from django.conf import settings


# the toolbar to use
CMS_TOOLBAR = getattr(
    settings,
    'CMS_TOOLBAR', 'minimalist_cms.cms_toolbar.cms_toolbar.CMSToolbar'
)


# enable/disable the edit mode feature
CMS_TOOLBAR_USE_EDIT_MODE = getattr(
    settings,
    'CMS_TOOLBAR_MENU', True
)
