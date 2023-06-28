from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from languages.forms import LanguageForm
from languages.models import Language
from trackings.models import Tracking

###############################
#######   C R E A T E   #######
###############################

class LanguageCreateView(CreateView):
    form_class = LanguageForm
    template_name = 'languages/create.html'
    success_url = reverse_lazy('languages:list')

    def dispatch(self, request, *args, **kwargs):
        if Tracking.is_last_version_released():
            messages.error(request, 'Add one open tracking before adding a Language')
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = self.success_url
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        l_id = Language.objects.all().values_list('id', flat=True)
        form.fields['id'].choices = (
            (k, v) for k, v in form.fields['id'].choices if k not in l_id)
        return form

    def form_valid(self, form):
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)

###############################
#########   L I S T   #########
###############################

class LanguageListView(ListView):
    model = Language
    template_name = 'languages/list.html'
    context_object_name = 'list_language'

###############################
#######   U P D A T E   #######
###############################

class LanguageUpdateView(UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = 'languages/update.html'
    success_url = reverse_lazy('languages:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = self.success_url
        context['url_delete'] = reverse_lazy('languages:delete', kwargs=dict(pk=self.kwargs['pk']))
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # To prevent from required error
        form.fields['id'].required=False
        form.fields['id'].widget.attrs['disabled'] = True
        return form

###############################
#######   D E L E T E   #######
###############################


class LanguageDeleteView(DeleteView):
    model = Language
    template_name = 'languages/delete.html'
    success_url = reverse_lazy('languages:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = self.success_url
        return context
