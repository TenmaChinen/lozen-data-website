from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from languages.forms import LanguageForm
from languages.models import Language
from django.urls import reverse_lazy
# from django.shortcuts import render

# Create
class LanguageCreateView(CreateView):
  form_class = LanguageForm
  template_name = 'languages/create.html'
  success_url = reverse_lazy('languages:list')

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['url_back'] = self.success_url
      return context
  
# Read
class LanguageListView(ListView):
  model = Language
  template_name = 'languages/list.html'
  context_object_name = 'list_language'


# Update
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

# Delete
class LanguageDeleteView(DeleteView):
  model = Language
  template_name = 'languages/delete.html'
  success_url = reverse_lazy('languages:list')

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['url_back'] = self.success_url
      return context
