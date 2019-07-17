from __future__ import unicode_literals

from django.http import Http404
from django.utils.translation import get_language
from django.views.generic import DetailView

from ..models import PageTranslation


class PageDetailView(DetailView):

    model = PageTranslation
    template_name = 'cms_pagetree/page_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['page'] = self.object.page
            context['paget_translation'] = self.object
        context.update(kwargs)
        return super(PageDetailView, self).get_context_data(**context)

    def get_object(self):
        qs = self.get_queryset()
        path = '/{}/'.format(self.request.LANGUAGE_CODE or get_language())
        slug = self.kwargs.get('slug')
        if slug:
            path = '{}{}/'.format(path, slug)
        try:
            obj = qs.get(path=path)
        except self.model.DoesNotExist:
            raise Http404()
        return obj

        print(path)
