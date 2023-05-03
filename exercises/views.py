from typing import Any, Dict, Optional, Type
from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from exercises.forms import ExerciseForm
from exercises.models import Exercise
from django.http import HttpResponse
from programs.models import Program

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import render
from io import StringIO
import pandas as pd

# Create
class ExerciseCreateView(CreateView):
  form_class = ExerciseForm
  template_name = 'exercises/create.html'

  # TODO : Document the "get_initial" override to initialize forms
  def get_initial(self):
    initial = super().get_initial()
    initial['week'] = self.kwargs['week']
    initial['day'] = self.kwargs['day']
    return initial

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update( self.kwargs ) # week & day
    return context

  # TODO : Document how to re-insert excluded form fields
  def form_valid(self, form):
    form.instance.program_id = self.kwargs['program_id']
    week, day = self.kwargs['week'], self.kwargs['day']
    exercises = Exercise.objects.filter(week=week, day=day)
    if exercises.exists():
      new_index = exercises.latest('index').index + 1
    else:
      new_index = 1
    
    form.instance.index = new_index
    form.instance.rest = form.cleaned_data['rest']

    return super().form_valid(form)

  def get_success_url(self):
    # TODO : Document that we can get the data defined in form is available here as "self.object"
    d_kwargs = {
      'program_id' : self.kwargs['program_id'],
      'week' : self.object.week,
      'day' : self.object.day
      }
    return reverse_lazy('exercises:list', kwargs=d_kwargs)


# Read
class ExerciseListView(ListView):
  model = Exercise
  template_name = 'exercises/list.html'
  context_object_name = 'list_exercise'

  # TODO : Document "get_queryset" override to filter ListView
  def get_queryset(self):
    queryset = super().get_queryset()
    program_id = self.kwargs['program_id']
    week = self.kwargs['week']
    day = self.kwargs['day']
    return queryset.filter(program_id=program_id, week=week, day=day)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context.update(self.kwargs)
      context['program'] = Program.objects.get(id=self.kwargs['program_id'])

      # TODO : Document how to get Form widgets or raw field 
      exercise_form_fields = ExerciseForm().fields
      week_widget = exercise_form_fields['week'].widget
      day_widget = exercise_form_fields['day'].widget
      
      # Forced attribute to track selected option ( invented attribute )
      week_widget.value = self.kwargs['week']
      day_widget.value = self.kwargs['day']

      context.update( dict( week_widget = week_widget, day_widget = day_widget ))

      context['base_url'] = self.request.path.split('?')[0]

      return context
  
# Update
class ExerciseUpdateView(UpdateView):
  model = Exercise
  form_class = ExerciseForm
  template_name = 'exercises/update.html'

  def get_success_url(self):
    week, day = self.object.week, self.object.day
    d_kwargs = dict( program_id = self.object.program.id, week=week, day=day )
    return reverse_lazy('exercises:list', kwargs=d_kwargs)

  # TODO : Document how to set values in form ( using get_initial )
  # def get_initial(self):
  #   initial = super().get_initial()
  #   rest_total_seconds = self.object.rest
  #   initial['rest_minutes'] = rest_total_seconds // 60
  #   initial['rest_seconds'] = rest_total_seconds % 60
  #   return initial

  # TODO : Document how to set values in form ( using get_form )
  def get_form(self):
    form = super().get_form(ExerciseForm)
    rest_total_seconds = form.instance.rest
    # rest_total_seconds = self.object.rest # This works as well
    form.fields['rest_minutes'].initial = rest_total_seconds // 60
    form.fields['rest_seconds'].initial = rest_total_seconds % 60
    
    return form

  # TODO : Document how to reasign exlucded form fields.
  def form_valid(self, form):
    form.instance.rest = form.cleaned_data['rest']
    return super().form_valid(form)


# Delete
class ExerciseDeleteView(DeleteView):
  model = Exercise
  template_name = 'exercises/delete.html'
  
  def get_success_url(self):
    d_kwargs = dict(
      program_id=self.object.program_id,
      week=self.object.week,
      day=self.object.day,
    )
    
    return reverse_lazy('exercises:list', kwargs=d_kwargs)


def exercise_upload_view(request,program_id):

  program = Program.objects.get(id=program_id)
  
  if request.method == 'GET':
    list_exercise = Exercise.objects.filter(program_id=program_id)
    list_exercise = list_exercise.order_by('week', 'day', 'index')
  
    l_field_name = Exercise.get_csv_fields()
    exercise_values = list_exercise.values(*l_field_name)
  
    # TODO : Document the "DataFrame.from_records"
    df_exercises = pd.DataFrame.from_records(data=exercise_values, columns=l_field_name)

    csv_exercises = df_exercises.to_csv(index=False)

    context = { 'program' : program, 'raw_csv' : csv_exercises }

    return render(request, 'exercises/upload.html', context)
  
  else:

    raw_csv = request.POST['raw_csv']
    raw_csv_io = StringIO(raw_csv)
    df_exercises = pd.read_csv(raw_csv_io)
    df_exercises.sort_values(by=['week','day'], inplace=True)
    
    l_instances = []
    index, last_week, last_day = 1, None, None

    # TODO : Document delete all in Django
    Exercise.objects.all().delete()

    for idx, row in df_exercises.iterrows():
      d_row = row.to_dict()
    
      instance = Exercise(program_id=program_id, index=index, **d_row )
      l_instances.append(instance)
      
      if row.week != last_week or row.day != last_day:
        index =  1
        last_week = row.week
        last_day = row.day
      else:
        index += 1

      # print(f'week : {row.week} | Day : {row.day} | idx : {index}')

    # TODO : Document the "Model.objects.bulk_create"
    # ( fast way to create multiple instances without using save() per each instance )
    Exercise.objects.bulk_create(l_instances)

    return redirect('exercises:list', program_id=program_id, week=1, day=1)


def exercise_download(request, program_id):
  if request.method == 'GET':
    response = HttpResponse(content_type='text/csv')
    file_name = f'program_exercises_id_{program_id}.csv'
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'


    exercises = Exercise.objects.filter(program_id=program_id)
    
    l_field_name = Exercise.get_csv_fields()
    exercises_values = exercises.values(*l_field_name)

    df_exercises = pd.DataFrame.from_records(data=exercises_values, columns=l_field_name)
    raw_csv = df_exercises.to_csv(index=False)
    response.write(raw_csv)

    return response
