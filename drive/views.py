from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic

from .models import PublicFile, PrivateFile
from .forms import FileForm


class IndexView(generic.TemplateView):
    template_name = 'drive/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = '{}.{}'.format(settings.VERSION, settings.PATCH_VERSION)
        return context


class DriveView(generic.FormView):
    template_name = 'drive/drive.html'
    form_class = FileForm
    success_url = '.'

    def form_valid(self, form):
        form.file.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['debug'] = settings.TEMPLATE_DEBUG
        context['public'] = PublicFile.objects.all()
        context['private'] = PrivateFile.objects.all()
        return context


class PublicDeleteView(generic.edit.DeleteView):
    model = PublicFile
    success_url = reverse_lazy('drive')


class PrivateDeleteView(generic.edit.DeleteView):
    model = PrivateFile
    success_url = reverse_lazy('drive')
