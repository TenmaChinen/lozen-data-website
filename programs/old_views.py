from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

from programs.forms import FormProgram, FormProgramTranslation
from programs.models import Program, ProgramTranslation
from trainings.models import Training
from languages.models import Language
from django.urls import reverse_lazy
from django.shortcuts import render

# Create

def program_create_view(request,training_id, language_id):
   
  training = Training.objects.get(id=training_id)
  language = Language.objects.get(id=language_id)
  
  if request.method == 'GET':
    form_program_translation = FormProgramTranslation()
    form_program_translation.fields['language_id'] = language_id
    context = dict(
      training=training,
      form_program = FormProgram(),
      form_program_translation = form_program_translation
      )
    return render(request, 'programs/create.html', context)

  else:
    # TODO : Document how to "reverse_lazy" from functional view
    d_kwargs = dict( training=training, language=language )
    return reverse_lazy('programs:list', kwargs=d_kwargs )

# class ProgramCreateView(CreateView):
#   form_class = FormProgram
#   template_name = 'programs/create.html'

#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context['training_id'] = self.kwargs['training_id']
#       return context

#   def form_valid(self, form):
#      form.instance.training_id = self.kwargs['training_id']
#      return super().form_valid(form)
  
#   def get_success_url(self):
#      d_kwargs = { 'training_id' : self.object.training_id }
#      return reverse_lazy('programs:list', kwargs=d_kwargs)
  

class ProgramDetailView(DetailView):
  model = Program
  template_name = 'programs/detail.html'
  context_object_name = 'program'

  # def get_context_data(self, **kwargs):
  #     context = super().get_context_data(**kwargs)
      
  #     context['training'] = Training.objects.get( id=self.kwargs['training_id'])
  #     return context

# Read
class ProgramListView(ListView):
  model = Program
  template_name = 'programs/list.html'
  context_object_name = 'list_program'
  
  def get_queryset(self):
    queryset = super().get_queryset()
    training_id = self.kwargs['training_id']
    return queryset.filter(training_id=training_id)	

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['training'] = Training.objects.get( id=self.kwargs['training_id'])
      return context

# Update
class ProgramUpdateView(UpdateView):
  model = Program
  form_class = FormProgram

  success_url = reverse_lazy('programs:list')
  template_name = 'programs/update.html'
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['training_id'] = self.object.training.id
      return context

  # def form_valid(self, form):
  #    form.instance.training_id = self.kwargs['training_id']
  #    return super().form_valid(form)
  
  def get_success_url(self):
     d_kwargs = { 'training_id' : self.object.training.id }
     return reverse_lazy('programs:list', kwargs=d_kwargs)


# Delete
class ProgramDeleteView(DeleteView):
  model = Program
  template_name = 'programs/delete.html'


  def get_success_url(self):
    d_kwargs = { 'training_id' : self.object.training.id }
    return reverse_lazy('programs:list', kwargs=d_kwargs)