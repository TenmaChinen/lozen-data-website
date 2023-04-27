from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from trainings.forms import TrainingForm
from trainings.models import Training
from django.urls import reverse_lazy
from django.shortcuts import render

# Create
class TrainingCreateView(CreateView):
  form_class = TrainingForm
  template_name = 'trainings/create.html'
  success_url = reverse_lazy('trainings:list')


# Read
class TrainingListView(ListView):
  model = Training
  template_name = 'trainings/list.html'
  context_object_name = 'training_list'


# Update
class TrainingUpdateView(UpdateView):
  model = Training
  form_class = TrainingForm

  success_url = reverse_lazy('trainings:list')
  template_name = 'trainings/update.html'

# Delete
class TrainingDeleteView(DeleteView):
  model = Training
  template_name = 'trainings/delete.html'
  success_url = reverse_lazy('trainings:list')
