from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from trainings_translations.forms import FormTrainingTranslation
from trainings_translations.models import TrainingTranslation
from languages.forms import LanguageForm
from trainings.models import Training

from trackings.models import Tracking

###############################
#######   D E T A I L   #######
###############################

def training_translation_detail_view(request, training_id, language_id):

    training = Training.objects.get(id=training_id)
    queryset = TrainingTranslation.objects.filter(training_id=training_id, language_id=language_id)
    if queryset.exists():
        training_translation = queryset.first()
    else:
        training_translation = TrainingTranslation(training_id=training_id, language_id=language_id)
        training_translation.version = Tracking.get_last_version()
        training_translation.save()

    context = dict(
        training = training,
        language_id = language_id,
        training_translation = training_translation,
        language_widget=LanguageForm.get_language_widget(language_id=language_id),
        url_back=reverse_lazy('trainings:list', kwargs=dict(language_id=language_id)),
    )

    return render(request, 'trainings_translations/detail.html', context)

###############################
#######   U P D A T E   #######
###############################

def training_translation_update_view(request, training_id, language_id):
    
    training = Training.objects.get(id=training_id)
    url_success = reverse_lazy('trainings:list', kwargs=dict(language_id=language_id))
    
    last_version = Tracking.get_last_version()
    if last_version == -1:
          return redirect(url_success)
    
    query = TrainingTranslation.objects.filter(training_id=training_id, language_id=language_id)
    if query.exists():
        training_translation = query.first()
    else:
        training_translation = TrainingTranslation(training_id=training_id, language_id=language_id)
        training_translation.version = last_version
        training_translation.save()

    ###################
    ###   P O S T   ###
    ###################
    
    if request.method == 'POST':
        d_data = request.POST
        form_training_translation = FormTrainingTranslation(data=d_data, instance=training_translation)
        form_training_translation.instance.version = last_version
        
        if form_training_translation.is_valid():
            form_training_translation.save()
            return redirect(url_success)
    else:
        ###################
        ####   G E T   ####
        ###################
        form_training_translation = FormTrainingTranslation(instance=training_translation)

    #########################
    ####   C O M M O N   ####
    #########################
    context = dict(
        unique_id=training.unique_id,
        form_training_translation=form_training_translation,
        url_back = url_success,
        url_delete = reverse_lazy('programs:delete', kwargs=dict(pk=training_id))
    )
    return render(request,'trainings_translations/update.html',context)