from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from languages.forms import LanguageForm
from programs.forms import FormProgram

from programs_translations.models import ProgramTranslation
from trainings.models import Training
from languages.models import Language
from programs.models import Program
from trackings.models import Tracking

import utils

###############################
#######   C R E A T E   #######
###############################

class ProgramCreateView(CreateView):
    form_class = FormProgram
    template_name = 'programs/create.html'

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          utils.add_open_track_message(request)
          return redirect(self.get_success_url())
      return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = self.get_success_url()
        return context

    def get_success_url(self):
        training_id = self.kwargs['training_id']
        return reverse_lazy('programs:list', kwargs=dict(training_id=training_id))
    
    def form_valid(self, form):
        training_id = self.kwargs['training_id']
        form.instance.training_id = training_id
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)

###############################
#######   D E T A I L   #######
###############################

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        training_id = self.object.training_id
        
        context.update(dict(
            url_back = reverse_lazy('programs:list', kwargs=dict(training_id=training_id)),
        ))
        return context


###############################
#########   L I S T   #########
###############################

def program_list_view(request, training_id, language_id=0):

    if not Language.objects.exists():
        utils.add_need_language_message(request)
        return redirect(reverse_lazy('languages:list'))

    language_id = utils.handle_language(request, language_id)
    last_version = Tracking.get_last_version()
    
    l_program_translation = []
    programs = Program.objects.filter(training_id=training_id)
    for program in programs:
        query = ProgramTranslation.objects.filter(program_id=program.id, language_id=language_id)
        if query.exists():
            program_translation = query.first()
        elif last_version != -1:
            program_translation = ProgramTranslation(program_id=program.id, language_id=language_id, version=last_version)
            program_translation.save()
        else:
            program_translation = None

        l_program_translation.append(program_translation)

    l_program = zip(programs, l_program_translation)

    context = dict(
        current_version=last_version,
        training=Training.objects.get(id=training_id),
        language=Language.objects.get(id=language_id),
        list_program=l_program,
        language_widget=LanguageForm.get_language_widget(language_id),
        url_back=reverse_lazy('trainings:list')
    )

    return render(request, 'programs/list.html', context)

###############################
#######   U P D A T E   #######
###############################

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = FormProgram
    template_name = 'programs/update.html'

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
        utils.add_open_track_message(request)
      return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        training_id = self.get_object().training_id
        return reverse_lazy('programs:list', kwargs=dict(training_id=training_id))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            training_id=self.object.training_id,
            url_back=self.get_success_url(),
            url_delete=reverse_lazy('programs:delete', kwargs=dict(pk=self.object.id))
        ))

        context['disabled'] = Tracking.is_last_version_released()

        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if Tracking.is_last_version_released():
            form.disable()
        return form

    def form_valid(self, form):
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)
    
###############################
#######   D E L E T E   #######
###############################

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'programs/delete.html'

    def dispatch(self, request, *args, **kwargs):
        if Tracking.is_last_version_released():
            utils.add_open_track_message(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        program = self.get_object()
        d_kwargs = dict(training_id=program.training.id)
        return reverse_lazy('programs:list', kwargs=d_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            dict(
            disabled=Tracking.is_last_version_released(),
            url_back=self.get_success_url(),
            ))
        return context