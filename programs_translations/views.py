from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.urls import reverse_lazy

from programs_translations.forms import FormProgramTranslation
from programs_translations.models import ProgramTranslation
from languages.forms import LanguageForm
from programs.models import Program

from trackings.models import Tracking

import utils

###############################
#######   D E T A I L   #######
###############################

def program_translation_detail_view(request, program_id, language_id=0):

    last_version = Tracking.get_last_version()
    language_id = utils.handle_language(request,language_id)

    program = Program.objects.get(id=program_id)
    queryset = ProgramTranslation.objects.filter(program_id=program_id, language_id=language_id)
    if queryset.exists():
        program_translation = queryset.first()
    elif last_version != -1:
        program_translation = ProgramTranslation(program_id=program_id, language_id=language_id)
        program_translation.version = last_version
        program_translation.save()
    else:
        program_translation = None

    context = dict(
        program = program,
        language_id = language_id,
        program_translation = program_translation,
        language_widget=LanguageForm.get_language_widget(language_id=language_id),
        url_back=reverse_lazy('programs:list', kwargs=dict(training_id=program.training_id)),
    )

    return render(request, 'programs_translations/detail.html', context)

###############################
#######   U P D A T E   #######
###############################

def program_translation_update_view(request, program_id, language_id=0):
    
    language_id = utils.handle_language(request,language_id)

    program = Program.objects.get(id=program_id)
    url_success = reverse_lazy('programs:list', kwargs=dict(training_id=program.training_id))
    
    last_version = Tracking.get_last_version()
    if last_version == -1:
        utils.add_open_track_message(request)
    
    query = ProgramTranslation.objects.filter(program_id=program_id, language_id=language_id)
    if query.exists():
        program_translation = query.first()
    elif last_version != -1:
        program_translation = ProgramTranslation(program_id=program_id, language_id=language_id)
        program_translation.version = last_version
        program_translation.save()
    else:
        program_translation = None

    ###################
    ###   P O S T   ###
    ###################
    
    if request.method == 'POST':
        d_data = request.POST
        form_program_translation = FormProgramTranslation(data=d_data, instance=program_translation)
        form_program_translation.instance.version = last_version
        
        if form_program_translation.is_valid():
            form_program_translation.save()
            return redirect(url_success)
    else:
        ###################
        ####   G E T   ####
        ###################
        
        form_program_translation = FormProgramTranslation(instance=program_translation)
        if last_version == -1:
            form_program_translation.disable()


    #########################
    ####   C O M M O N   ####
    #########################
    context = dict(
        disabled=last_version==-1,
        program=program,
        form_program_translation=form_program_translation,
        url_back = url_success,
        url_delete = reverse_lazy('programs:delete', kwargs=dict(pk=program_id))
    )
    return render(request,'programs_translations/update.html',context)