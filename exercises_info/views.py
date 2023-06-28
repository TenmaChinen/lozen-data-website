from typing import Optional, Type
from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from pandas import DataFrame
import json

from exercises_info_translations.models import ExerciseInfoTranslation
from exercises_info.forms import FormExerciseInfo
from exercises_info.models import ExerciseInfo
from trackings.models import Tracking
from languages.models import Language
from languages.forms import LanguageForm
from programs.models import Program

import utils

###############################
#######   C R E A T E   #######
###############################

class ExerciseInfoCreateView(CreateView):
    form_class = FormExerciseInfo
    template_name = 'exercises_info/create.html'
    success_url = reverse_lazy('exercises_info:list')

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          utils.add_open_track_message(request)
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_id'] = ExerciseInfo.get_new_id()
        context['url_cancel'] = self.get_success_url()
        return context
    
    def form_valid(self, form):
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)
    
    def get_success_url(self):
        d_kwargs = dict( language_id =  self.request.session.get( 'language_id', 1))
        return reverse_lazy('exercises_info:list', kwargs = d_kwargs)

###############################
#########   L I S T   #########
###############################

# TODO : Add some Increase version for All ( Parent or Translations ) button
# In case we add a new field

def exercise_info_list_view(request, language_id=0):

    if not Language.objects.exists():
        messages.error(request, 'You need to add at least one Language')
        return redirect(reverse_lazy('languages:list'))
    
    if language_id == 0:
        language_id = get_session_language(request)

    last_version = Tracking.get_last_version()
    exercises_info = ExerciseInfo.objects.all().order_by('id')
    
    l_exercise_info_translation = []
    
    for exercise_info in exercises_info:
        query = ExerciseInfoTranslation.objects.filter(exercise_info_id=exercise_info.id, language_id=language_id)
        if query.exists():
            program_translation = query.first()
        elif last_version != -1:
            program_translation = ExerciseInfoTranslation(exercise_info_id=exercise_info.id, language_id=language_id, version=last_version)
            program_translation.save()
        else:
            program_translation = None

        l_exercise_info_translation.append(program_translation)

    l_exercise_info = zip(exercises_info, l_exercise_info_translation)
    
    context = dict(
        language=Language.objects.get(id=language_id),
        list_exercise_info=l_exercise_info,
        language_widget=LanguageForm.get_language_widget(language_id),
        add_button_disabled = Tracking.is_last_version_released(),
        current_version = Tracking.get_last_version()
    )

    return render(request, 'exercises_info/list.html', context)

###############################
#######   D E T A I L   #######
###############################

class ExerciseInfoDetailView(DetailView):
    model = ExerciseInfo
    template_name = 'exercises_info/detail.html'
    context_object_name = 'exercise_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            url_back = reverse_lazy('exercises_info:list')
        ))
        return context

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
          utils.add_open_track_message(request)
      return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if Tracking.is_last_version_released():
            form.disable()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            disabled = Tracking.is_last_version_released(),
            exercise_info_id = self.object.id,
            url_back=self.success_url,
            url_delete=reverse_lazy('exercises_info:delete', kwargs=dict(pk=self.object.id))
        ))
        return context

###############################
#######   D E L E T E   #######
###############################

class ExerciseInfoDeleteView(DeleteView):
    model = ExerciseInfo
    template_name = 'exercises_info/delete.html'
    context_object_name = 'exercise_info'
    
    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          utils.add_open_track_message(request)
      return super().dispatch(request, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update( dict(
            disabled = Tracking.is_last_version_released(),
            exercise_info_id = self.object.id,
            url_back = self.get_success_url()
        ))
        return context

    def get_success_url(self):
        d_kwargs = dict(language_id=get_session_language(self.request))
        return reverse_lazy('exercises_info:list', kwargs=d_kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return super().delete(request, *args, **kwargs)

###############################
#######   U P L O A D   #######
###############################

def exercise_info_upload_view(request):

    url_back = reverse_lazy('exercises_info:list', kwargs=dict(language_id=1))
    last_tracking_version = Tracking.get_last_version()
    if last_tracking_version == -1:
        utils.add_open_track_message(request)
        return redirect(url_back)

    ###################
    ####   G E T   ####
    ###################
    if request.method == 'GET':
        d_raw_json = get_exercises_info_dict()
        raw_json = json.dumps(d_raw_json, indent=2, ensure_ascii=False)
        context = {'raw_json': raw_json, 'url_back' : url_back }
        return render(request, 'exercises_info/upload.html', context)
    
    ###################
    ###   P O S T   ###
    ###################
    else:
        d_data = request.POST
        d_language = dict(Language.objects.all().values_list('abbreviation','id'))

        try:
            raw_json = d_data['raw_json']
            d_raw_json = json.loads(raw_json)
        
            for _id, d_exercise_info in d_raw_json.items():
                _id = int(_id)
                
                # TODO : Document "get_or_create" ( if create=True doesn't need save )
                exercise_info, is_created = ExerciseInfo.objects.get_or_create(id=_id, defaults=dict(version=last_tracking_version))
                exercise_info.unique_id = d_exercise_info['unique_id']
                exercise_info.save()
    
                # file_name = d_exercise_info['file_name']

                for language_abbreviation, d_translation in d_exercise_info['translations'].items():
                    language_id = d_language[language_abbreviation]
                    d_defaults = dict(version=last_tracking_version)
                    exercise_info_translation, is_created = ExerciseInfoTranslation.objects.get_or_create(exercise_info_id=_id, language_id=language_id, defaults=d_defaults)
                    exercise_info_translation.title = d_translation['title']
                    exercise_info_translation.description = d_translation['description']
                    exercise_info_translation.version = last_tracking_version
                    exercise_info_translation.save()

            return redirect(url_back)
        
        except json.decoder.JSONDecodeError as e:
            context = {'raw_json': raw_json}
            return render(request, 'exercises_info/upload.html', context)

###############################
########   U T I L S   ########
###############################

def get_exercises_info_dict():
    
    queryset = ExerciseInfo.objects.all()
    if queryset.exists():
        values = queryset.values('id','unique_id', 'unit_type')
        d_parent = DataFrame(data=values)
        d_parent.set_index('id', inplace=True)
        d_raw = d_parent.to_dict(orient='index')
        for k in d_raw:
            d_raw[k]['translations'] = {}
    
        l_field_name = [ field.get_attname() for field in ExerciseInfoTranslation._meta.get_fields() ]
        l_field_name = [ f for f in l_field_name  if f not in ['id','version','language_id'] ]
        values = ExerciseInfoTranslation.objects.all().values(*l_field_name, 'language__abbreviation')
        d_exercise_info_translations = DataFrame(data=values)
        
        for exercise_info_id, df_group in d_exercise_info_translations.groupby('exercise_info_id'):
            df_group.drop('exercise_info_id', axis=1, inplace=True)
            for language_id, d_record in df_group.groupby('language__abbreviation'):
                d_record.drop('language__abbreviation', axis=1, inplace=True)
                d_raw[exercise_info_id]['translations'][language_id] = d_record.squeeze().to_dict()

        return d_raw
    return {}


def get_session_language(request):
   return request.session.get('language_id',1)