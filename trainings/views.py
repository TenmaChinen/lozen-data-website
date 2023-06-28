from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages

from trainings.forms import TrainingForm
from trainings_translations.models import TrainingTranslation
from languages.models import Language
from languages.forms import LanguageForm
from trainings.models import Training
from trackings.models import Tracking

import utils

###############################
#######   C R E A T E   #######
###############################


class TrainingCreateView(CreateView):
  form_class = TrainingForm
  template_name = 'trainings/create.html'
  success_url = reverse_lazy('trainings:list')

  def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          utils.add_open_track_message(request)
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    return context

  def form_valid(self, form):
    form.instance.version = Tracking.get_last_version()
    return super().form_valid(form)

###############################
#########   L I S T   #########
###############################

def training_list_view(request, language_id=0):

    if not Language.objects.exists():
        utils.add_need_language_message(request)
        return redirect(reverse_lazy('languages:list'))

    language_id = utils.handle_language(request, language_id)
    last_version = Tracking.get_last_version()
    l_training_translation = []
    trainings = Training.objects.all()

    for training in trainings:
        query = TrainingTranslation.objects.filter(
            training_id=training.id, language_id=language_id)
        if query.exists():
            training_translation = query.first()
        elif last_version != -1:
            training_translation = TrainingTranslation(
                training_id=training.id, language_id=language_id, version=last_version)
            training_translation.save()
        else:
            training_translation = None

        l_training_translation.append(training_translation)

    l_training = zip(trainings, l_training_translation)

    context = dict(
        current_version=last_version,
        language=Language.objects.get(id=language_id),
        list_training=l_training,
        language_widget=LanguageForm.get_language_widget(language_id),
        url_back=reverse_lazy('languages:list')
    )

    return render(request, 'trainings/list.html', context)


###############################
#######   D E T A I L   #######
###############################

def training_detail_view(request, training_id):

    training = Training.objects.get(id=training_id)
    context = dict(
        training=training,
        url_back=reverse_lazy('trainings:list'),
    )

    return render(request, 'trainings/detail.html', context)

###############################
#######   U P D A T E   #######
###############################


class TrainingUpdateView(UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = 'trainings/update.html'
    success_url = reverse_lazy('trainings:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_cancel'] = self.success_url
        context['url_delete'] = reverse_lazy('trainings:delete', kwargs=dict(pk=self.kwargs['pk']))
        
        if Tracking.is_last_version_released():
            utils.add_open_track_message(self.request)
            context['disabled'] = True
        else:
            context['disabled'] = False
            
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if Tracking.is_last_version_released():
            form.fields['unique_id'].widget.attrs['disabled'] = True
        return form

    def form_valid(self, form):
        form.instance.version = Tracking.get_last_version()
        return super().form_valid(form)

###############################
#######   D E L E T E   #######
###############################

class TrainingDeleteView(DeleteView):
    model = Training
    template_name = 'trainings/delete.html'
    success_url = reverse_lazy('trainings:list')

    def dispatch(self, request, *args, **kwargs):
        if Tracking.is_last_version_released():
            utils.add_open_track_message(request)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_cancel'] = self.success_url
        context['disabled'] = Tracking.is_last_version_released()
        return context