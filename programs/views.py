from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView

from programs.forms import FormProgram, FormProgramTranslation
from programs.models import Program, ProgramTranslation
from django.shortcuts import render, redirect
from languages.forms import LanguageForm
from trainings.models import Training
from languages.models import Language
from django.urls import reverse_lazy
from django.contrib import messages

###############################
#######   C R E A T E   #######
###############################

def program_create_view(request,training_id, language_id):
   
  training = Training.objects.get(id=training_id)
  language = Language.objects.get(id=language_id)
  
  # TODO : Document how to "reverse_lazy" from functional view
  url_success = reverse_lazy('programs:list', kwargs=dict( training_id=training_id, language_id=language_id ))
  
  if request.method == 'POST':
  
    d_data = request.POST
    form_program = FormProgram(data=d_data)
    form_program_translation = FormProgramTranslation(data=d_data)

    form_program.instance.training_id = training_id
    if form_program.is_valid():
      new_program = form_program.save()

      form_program_translation.instance.program_id = new_program.id
      if form_program_translation.is_valid():
        form_program_translation.save()

        return redirect(url_success)

  else:
    ###################
    ####   G E T   ####
    ###################
    form_program = FormProgram()
    form_program.fields['unique_id'].initial = 1

    form_program_translation = FormProgramTranslation()
    form_program_translation.fields['language'].initial = language
    
  context = dict(
    training=training,
    language_id=language_id,
    form_program = form_program,
    form_program_translation = form_program_translation,
    url_back=url_success
  )
  return render(request, 'programs/create.html', context)

###############################
#######   D E T A I L   #######
###############################

def program_detail_view(request, program_id, language_id):
  
  program = Program.objects.get(id=program_id)
  program_translation = ProgramTranslation.objects.get(program_id=program_id, language_id=language_id)

  context = dict(
    training_id=program.training_id,
    language_id=language_id,
    program = program,
    program_translation = program_translation,
    language_widget =  LanguageForm.get_language_widget(language_id),
    )
  
  return render(request, 'programs/detail.html', context)

###############################
#########   L I S T   #########
###############################

def program_list_view(request,training_id, language_id):
  
  url_back = reverse_lazy('trainings:list')

  if not Language.objects.exists():
    # TODO : Document the messages error
    message = 'You need to add at least one Language'
    # messages.add_message(request, messages.ERROR, message)
    messages.error(request, message)
    return redirect(url_back)

  l_program_translation = []
  programs = Program.objects.filter(training_id=training_id)
  for program in programs:
    query = ProgramTranslation.objects.filter(program_id=program.id, language_id=language_id)
    if query.exists():
      program_translation = query.first()
    else:
      program_translation = ProgramTranslation(program_id=program.id, language_id=language_id)
      program_translation.save()

    l_program_translation.append(program_translation)

  l_program = zip(programs, l_program_translation)

  context = dict(
    training = Training.objects.get(id=training_id),
    language = Language.objects.get(id=language_id),
    list_program = l_program,
    language_widget =  LanguageForm.get_language_widget(language_id),
    url_back=url_back
  )

  return render(request, 'programs/list.html', context)

# TODO : Check if this is possible and Document if so
# return queryset.filter(program__training__id=training_id, language_id=language_id)	
# return queryset.filter(program__training__id=training_id)	


###############################
#######   U P D A T E   #######
###############################

def program_update_view(request, program_id, language_id):

  program = Program.objects.get(id=program_id)

  query = ProgramTranslation.objects.filter(program_id=program_id, language_id=language_id)
  if query.exists():
    program_translation = query.first()
  else:
    program_translation = ProgramTranslation(program_id=program_id, language_id=language_id)
    program_translation.save()

  url_back = reverse_lazy('programs:list', kwargs=dict( training_id=program.training_id, language_id=language_id ))
  
  if request.method == 'POST':
    d_data = request.POST

    form_program = FormProgram(data=d_data, instance=program)
    if form_program.is_valid():
      form_program.save()
    
    form_program_translation = FormProgramTranslation(data=d_data, instance=program_translation)
    if form_program_translation.is_valid():
      form_program_translation.save()

    return redirect(url_back)
  
  else:
    ###################
    ####   G E T   ####
    ###################

    # TODO : Document how to fill a form with the model instance
    form_program = FormProgram(instance=program)
    form_program_translation = FormProgramTranslation(instance=program_translation)

  #########################
  ####   C O M M O N   ####
  #########################

  url_delete = reverse_lazy('programs:delete', kwargs=dict(program_id=program_id, language_id=language_id))

  context = dict(
    training_id = program.training_id,
    program_id = program_id,
    language_id = language_id,
    form_program = form_program,
    form_program_translation = form_program_translation,
    url_back = url_back,
    url_delete = url_delete,
  )
  
  return render(request, 'programs/update.html', context)

###############################
#######   D E L E T E   #######
###############################

class ProgramDeleteView(DeleteView):
  model = Program
  template_name = 'programs/delete.html'


  def get_success_url(self):
    d_kwargs = { 'training_id' : self.object.training.id }
    return reverse_lazy('programs:list', kwargs=d_kwargs)