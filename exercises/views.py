from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from exercises.forms import ExerciseForm
from exercises.models import Exercise
from django.urls import reverse_lazy
from weeks_days.models import Day

# Create


class ExerciseCreateView(CreateView):
  form_class = ExerciseForm
  template_name = 'exercises/create.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['day'] = Day.objects.get(id=self.kwargs['day_id'])
    return context

  def form_valid(self, form):
    form.instance.day_id = self.kwargs['day_id']
    exercises = Exercise.objects.filter(day_id=self.kwargs['day_id'])
    if exercises.exists():
      new_idx = exercises.latest('idx').idx + 1
    else:
      new_idx = 1
    
    form.instance.idx = new_idx
    return super().form_valid(form)

  def get_success_url(self):
    d_kwargs = { 'day_id' : self.object.day.id }
    return reverse_lazy('exercises:list', kwargs=d_kwargs)


# Read
class ExerciseListView(ListView):
  model = Exercise
  template_name = 'exercises/list.html'
  context_object_name = 'list_exercise'

  # To query the exercises related to the program id
  def get_queryset(self):
    queryset = super().get_queryset()
    day_id = self.kwargs['day_id']
    return queryset.filter(day_id=day_id)	

  # To put the program instance to the context
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['day'] = Day.objects.get( id=self.kwargs['day_id'])
      return context