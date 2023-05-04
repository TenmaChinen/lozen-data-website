from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from trainings.forms import TrainingForm
from trainings.models import Training
from django.urls import reverse_lazy

# Create
class TrainingCreateView(CreateView):
  form_class = TrainingForm
  template_name = 'trainings/create.html'
  success_url = reverse_lazy('trainings:list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    return context



# Read
class TrainingListView(ListView):
  model = Training
  template_name = 'trainings/list.html'
  context_object_name = 'list_training'


# Update
class TrainingUpdateView(UpdateView):
  model = Training
  form_class = TrainingForm
  success_url = reverse_lazy('trainings:list')
  template_name = 'trainings/update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    context['url_delete'] = reverse_lazy('trainings:delete', kwargs=dict(pk=self.kwargs['pk']))
    return context

# Delete
class TrainingDeleteView(DeleteView):
  model = Training
  template_name = 'trainings/delete.html'
  success_url = reverse_lazy('trainings:list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    return context
