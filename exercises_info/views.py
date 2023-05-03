from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from exercises_info.forms import ExerciseInfoForm
from exercises_info.models import ExerciseInfo
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
import json

# Create
class ExerciseInfoCreateView(CreateView):
  form_class = ExerciseInfoForm
  template_name = 'exercises_info/create.html'
  success_url = reverse_lazy('exercises_info:list')

  def form_valid(self, form):
    form.instance.id = ExerciseInfo.get_new_id()
    return super().form_valid(form)

# Read
class ExerciseInfoListView(ListView):
  model = ExerciseInfo
  template_name = 'exercises_info/list.html'
  context_object_name = 'list_exercise_info'

class ExerciseInfoDetailView(DetailView):
  model = ExerciseInfo
  template_name = 'exercises_info/detail.html'
  context_object_name = 'exercise_info'

# Update
class ExerciseInfoUpdateView(UpdateView):
  model = ExerciseInfo
  form_class = ExerciseInfoForm
  template_name = 'exercises_info/update.html'
  context_object_name = 'exercise_info'
  success_url = reverse_lazy('exercises_info:list')

# Delete
class ExerciseInfoDeleteView(DeleteView):
  model = ExerciseInfo
  template_name = 'exercises_info/delete.html'
  context_object_name = 'exercise_info'
  success_url = reverse_lazy('exercises_info:list')


# Upload
def exercise_info_upload_view(request):
  
  if request.method == 'GET':
    d_raw_json = get_d_raw_json()
    raw_json = json.dumps(d_raw_json, indent=2)
    context = { 'raw_json' : raw_json }
    return render(request, 'exercises_info/upload.html',context)
  else:
    data = request.POST
    
    try:
      raw_json = data['raw_json']
      d_raw_json = json.loads(raw_json)

      ExerciseInfo.objects.all().delete()
      
      for _id, d_values in d_raw_json.items():
        title = d_values['title']
        description = d_values['description']
        exercise_info = ExerciseInfo(id=_id, title=title, description=description)
        exercise_info.save()

      return redirect('exercises_info:list')
    except json.decoder.JSONDecodeError as e:
      context = { 'raw_json' : raw_json }
      return render(request, 'exercises_info/upload.html',context)

# Download
def exercise_info_download(request):
  if request.method == 'GET':
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="exercises_info.json'

    d_raw_json = get_d_raw_json()  
    json.dump(d_raw_json, response, indent=2)
    return response


# Utils
def get_d_raw_json():
  d_raw_json = {}
  for exercise_info in ExerciseInfo.objects.all():
    d_raw_json[exercise_info.id] = dict(
      title = exercise_info.title,
      description = exercise_info.description 
      )
  return d_raw_json