import importlib

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from minimalist_cms.cms_toolbar import conf


register = template.Library()

# TODO cleanup
@register.inclusion_tag('cms_toolbar/toolbar.html', takes_context=True)
def cms_toolbar(context):
    # first, check the GET
    request = context['request']
    if 'edit' in request.GET:
        request.session['cms_toolbar_edit'] = True
    if 'edit_off' in request.GET:
        if 'cms_toolbar_edit' in request.session:
            del(request.session['cms_toolbar_edit'])
    # import toolbar class
    (toolbar_module_path, toolbar_cls_name) = conf.CMS_TOOLBAR.rsplit('.', 1)
    try:
        toolbar_module = importlib.import_module(toolbar_module_path)
    except ImportError:
        msg = "Error importing cms toolbar! ({})".format(settings.CMS_TOOLBAR)
        raise ImproperlyConfigured(msg)
    toolbar_cls = getattr(toolbar_module, toolbar_cls_name, None)
    if not toolbar_cls:
        msg = "Error importing cms toolbar! ({})".format(settings.CMS_TOOLBAR)
        raise ImproperlyConfigured(msg)
    toolbar = toolbar_cls()
    context['toolbar_menu'] = toolbar.get_menu(request)
    return context


@register.simple_tag(takes_context=True)
def cms_toolbar_edit_link(context, model_instance, edit_text=''):
    """
    edit link, opens dialog to edit provided model (or create new,
    when passed a model class) :return:s
    """
    if not context['request'].session.get('cms_toolbar_edit', None):
        return ''
    if not edit_text:
        edit_text = _('Edit')

    opts = model_instance._meta
    # Django < 1.10 creates dynamic proxy model subclasses when fields are
    # deferred using .only()/.exclude(). Make sure to use the underlying
    # model options when it's the case.
    if getattr(model_instance, '_deferred', False):
        opts = opts.proxy_for_model._meta
    edit_link = reverse(
        'admin:{}_{}_change'.format(opts.app_label, opts.model_name),
        args=(model_instance.id,)
    )

    return mark_safe(
        '<a href="{}" class="minimalist-cms-edit-link">{}</a>'.format(
            edit_link,
            edit_text
        )
    )
