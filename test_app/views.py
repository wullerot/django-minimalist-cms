from django.views.generic import \
    ListView

from test_app.models import TestModel


class TestModelView(ListView):
    model = TestModel
