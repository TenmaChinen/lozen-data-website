from typing import Optional, Type
from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
import json

from exercises_info.forms import FormExerciseInfo
from exercises_info.models import ExerciseInfo
from trackings.models import Tracking

###############################
#######   C R E A T E   #######
###############################

class ExerciseInfoCreateView(CreateView):
    form_class = FormExerciseInfo
    template_name = 'exercises_info/create.html'
    success_url = reverse_lazy('exercises_info:list')

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          messages.error(request,'Add one open tracking before adding a new "Exercise Info"')
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.initial['id'] = ExerciseInfo.get_new_id()
        return form

    def form_valid(self, form):
        form.instance.id = ExerciseInfo.get_new_id()
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)

###############################
#########   L I S T   #########
###############################

class ExerciseInfoListView(ListView):
    model = ExerciseInfo
    template_name = 'exercises_info/list.html'
    context_object_name = 'list_exercise_info'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            add_button_disabled = Tracking.is_last_version_released(),
            current_version = Tracking.get_last_version()
        ))
        return context
    

###############################
#######   D E T A I L   #######
###############################

class ExerciseInfoDetailView(DetailView):
    model = ExerciseInfo
    template_name = 'exercises_info/detail.html'
    context_object_name = 'exercise_info'

###############################
#######   U P D A T E   #######
###############################

class ExerciseInfoUpdateView(UpdateView):
    model = ExerciseInfo
    form_class = FormExerciseInfo
    template_name = 'exercises_info/update.html'
    context_object_name = 'exercise_info'
    success_url = reverse_lazy('exercises_info:list')

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # TODO : Set the last version here
        return super().form_valid(form)

###############################
#######   D E L E T E   #######
###############################

class ExerciseInfoDeleteView(DeleteView):
    model = ExerciseInfo
    template_name = 'exercises_info/delete.html'
    context_object_name = 'exercise_info'
    success_url = reverse_lazy('exercises_info:list')
    
    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return super().delete(request, *args, **kwargs)

###############################
#######   U P L O A D   #######
###############################

def exercise_info_upload_view(request):

    url_back = reverse_lazy('exercises_info:list')
    last_tracking_version = Tracking.get_last_version()
    if last_tracking_version == -1:
        messages.error(request,'Add one open tracking before uploading "Exercise Info"')
        return redirect(url_back)

    ###################
    ####   G E T   ####
    ###################
    if request.method == 'GET':
        d_raw_json = get_d_raw_json()
        raw_json = json.dumps(d_raw_json, indent=2)
        context = {'raw_json': raw_json}
        return render(request, 'exercises_info/upload.html', context)
    
    ###################
    ###   P O S T   ###
    ###################
    else:
        d_data = request.POST

        try:
            raw_json = d_data['raw_json']
            d_raw_json = json.loads(raw_json)

            s_uploaded_ids = { int(_id) for _id in d_raw_json }
            s_saved_ids = { int(_id) for _id in ExerciseInfo.objects.all().values_list('id', flat=True) }

            s_reused_ids = s_uploaded_ids.intersection(s_saved_ids)
            s_new_ids = s_uploaded_ids.difference(s_saved_ids)
            print('Saved IDs : ',s_saved_ids)
            print('Reused : ',s_reused_ids)
            print('New Ids : ', s_new_ids)

            # Update Reused IDs
            for reused_id in s_reused_ids:
                exercise_info = ExerciseInfo.objects.get(id=reused_id)
                
                for key, value in d_raw_json[str(reused_id)].items():
                    if key == 'id': continue
                    setattr(exercise_info, key, value)
                exercise_info.version = last_tracking_version
                exercise_info.save()

            # Create New IDs
            for new_id in s_new_ids:
                d_exercise_info_data = d_raw_json[str(new_id)]
                form_exercise_info = FormExerciseInfo(data=d_exercise_info_data)
                form_exercise_info.data['id'] = new_id
                form_exercise_info.instance.id = new_id
                form_exercise_info.instance.version = last_tracking_version
                if form_exercise_info.is_valid():
                    form_exercise_info.save()
                else:
                    # TODO : Append as another table the non uploaded rows in red.
                    print('Form error : ' + form_exercise_info.errors)

            return redirect(url_back)
        
        except json.decoder.JSONDecodeError as e:
            context = {'raw_json': raw_json}
            return render(request, 'exercises_info/upload.html', context)

###############################
#####   D O W N L O A D   #####
###############################

def exercise_info_download(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="exercises_info.json'

        d_raw_json = get_d_raw_json()
        json.dump(d_raw_json, response, indent=2)
        return response

###############################
########   U T I L S   ########
###############################

def get_d_raw_json():
    d_raw_json = {}
    for exercise_info in ExerciseInfo.objects.all():
        d_raw_json[exercise_info.id] = dict(
            title=exercise_info.title,
            description=exercise_info.description
        )
    return d_raw_json