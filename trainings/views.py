from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from trainings.forms import TrainingForm
from trainings.models import Training
from trackings.models import Tracking

###############################
#######   C R E A T E   #######
###############################

class TrainingCreateView(CreateView):
  form_class = TrainingForm
  template_name = 'trainings/create.html'
  success_url = reverse_lazy('trainings:list')

  def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          messages.error(request,'Add one open tracking before adding a Training')
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    return context
  
  def form_valid(self, form):
    form.instance.version = Tracking.get_last_version()
    return super().form_valid(form)

###############################
#########   L I S T   #########
###############################

class TrainingListView(ListView):
  model = Training
  template_name = 'trainings/list.html'
  context_object_name = 'list_training'

###############################
#######   U P D A T E   #######
###############################

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
  
  def form_valid(self, form):
    form.instance.version = Tracking.get_last_version()
    return super().form_valid(form)

###############################
#######   D E L E T E   #######
###############################

class TrainingDeleteView(DeleteView):
  model = Training
  template_name = 'trainings/delete.html'
  success_url = reverse_lazy('trainings:list')

  def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    return context