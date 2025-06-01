from django.http import HttpResponse
from django.views.generic import TemplateView

class AdminStyleTestView(TemplateView):
    template_name = 'admin/style_test.html'
