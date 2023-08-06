from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Home view for our pypipackage.
    """
    template_name = 'pypipackage/home.html'
