# django-mini-cms

The minimalist cms, with four plugable core modules. That are

- (basic implementation done) A toolbar for your frontend, allows login/logout, and model editing directly in the frontend
- (to be done) A dynamic content framework, for hierarchical content on any model, always based on the same content types
- (to be done) A page tree module, for building, yes, page trees
- (to be done, last) A publisher module, for adding a basic live/draft version separation, where the draft can then be published to live. for any model that wants it

All three are optional, whereas the toolbar is probably needed in most cases. This project is inspired by django-cms, but tries to avoid any magic and over complex things.


## Installation

To get the latest stable release from PyPi (not yet!)

    pip install django-minimalist-cms

Add your needed modules to to your ``INSTALLED_APPS``. See "Usage" for further details.

    INSTALLED_APPS = (
        ...,
        'minimalist_cms.cms_toolbar',
        'minimalist_cms.cms_pagetree',
        'minimalist_cms.cms_content',
        'minimalist_cms.cms_publisher',
    )


## Usage

### CMS Toolbar

Besides adding `minimalist_cms.cms_toolbar` to installed apps, you'll need to do the following:

#### Add the toolbar in your html

    {% load cms_toolbar_tags %}
    {% cms_toolbar %}

This will show the toolbar handle on the left side of the browser. If you want to add direct edit links, 
for your objects, add something like this:

    {% cms_toolbar_edit_link object_to_edit 'optional link text' %}
    
This will open the toolbar iframe, with the admin change view for the `object_to_edit`. Edit links will 
only be visible when in "Edit Mode".

#### Configure the toolbar menu

Use the setting `CMS_TOOLBAR` to define the class that should be your toolbar.

    CMS_TOOLBAR = 'yourapp.toolbar.CMSToooooolbarrrr'
    
It's very basic, looking at the following example and the resulting output, should make it clear:

    from django.urls import reverse
    
    class CMSToolbar(object):
    
        def get_menu(self, request):
            return [
                # name in handle
                {'name': 'Admin', 'menu': [
                        # menu section title
                        {'name': 'Admininstration', 'items': [
                                {
                                    # one link in menu
                                    'link': reverse('admin:sites_site_changelist'),
                                    'name': ("Sites"),
                                },
                                {
                                    'link': reverse('admin:auth_user_changelist'),
                                    'name': ("Users"),
                                },
                            ]
                        },
                    ]
                },
            ]
            
This is the basic toolbar, when you dont define an own one. Defined in `minimalist_cms/cms_toolbar/cms_toolbar.py`.

#### Toolbar settings

`CMS_TOOLBAR` as explained just above.

`CMS_TOOLBAR_USE_EDIT_MODE` use edit mode feature. Defaults to `True`