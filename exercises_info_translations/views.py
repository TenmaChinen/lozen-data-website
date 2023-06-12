from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from exercises_info_translations.forms import FormExerciseInfoTranslation
from exercises_info_translations.models import ExerciseInfoTranslation
from exercises_info.models import ExerciseInfo
from languages.forms import LanguageForm

from trackings.models import Tracking

###############################
#######   D E T A I L   #######
###############################

def exercise_info_translation_detail_view(request, exercise_info_id, language_id):

    exercise_info = ExerciseInfo.objects.get(id=exercise_info_id)
    queryset = ExerciseInfoTranslation.objects.filter(exercise_info_id=exercise_info_id, language_id=language_id)
    if queryset.exists():
        exercise_info_translation = queryset.first()
    else:
        exercise_info_translation = ExerciseInfoTranslation(exercise_info_id=exercise_info_id, language_id=language_id)
        exercise_info_translation.version = Tracking.get_last_version()
        exercise_info_translation.save()

    context = dict(
        exercise_info = exercise_info,
        language_id = language_id,
        exercise_info_translation = exercise_info_translation,
        language_widget=LanguageForm.get_language_widget(language_id=language_id),
        url_back=reverse_lazy('exercises_info:list', kwargs=dict(language_id=language_id)),
    )

    return render(request, 'exercises_info_translations/detail.html', context)

###############################
#######   U P D A T E   #######
###############################

def exercise_info_translation_update_view(request, exercise_info_id, language_id):
    
    url_success = reverse_lazy('exercises_info:list', kwargs=dict(language_id=language_id))
    
    last_version = Tracking.get_last_version()
    if last_version == -1:
          return redirect(url_success)
    
    query = ExerciseInfoTranslation.objects.filter(exercise_info_id=exercise_info_id, language_id=language_id)
    if query.exists():
        exercise_info_translation = query.first()
    else:
        exercise_info_translation = ExerciseInfoTranslation(exercise_info_id=exercise_info_id, language_id=language_id)
        exercise_info_translation.version = last_version
        exercise_info_translation.save()

    ###################
    ###   P O S T   ###
    ###################
    
    if request.method == 'POST':
        d_data = request.POST
        form_exercise_info_translation = FormExerciseInfoTranslation(data=d_data, instance=exercise_info_translation)
        form_exercise_info_translation.instance.version = last_version
        
        if form_exercise_info_translation.is_valid():
            form_exercise_info_translation.save()
            return redirect(url_success)
    else:
        ###################
        ####   G E T   ####
        ###################
        form_exercise_info_translation = FormExerciseInfoTranslation(instance=exercise_info_translation)

    #########################
    ####   C O M M O N   ####
    #########################
    context = dict(
        exercise_info=ExerciseInfo.objects.get(id=exercise_info_id),
        form_exercise_info_translation=form_exercise_info_translation,
        url_back = url_success,
        url_delete = reverse_lazy('exercises_info:delete', kwargs=dict(pk=exercise_info_id))
    )
    return render(request,'exercises_info_translations/update.html',context)