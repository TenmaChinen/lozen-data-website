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

###############################
#######   C R E A T E   #######
###############################

class TrainingCreateView(CreateView):
  form_class = TrainingForm
  template_name = 'trainings/create.html'

  def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          messages.error(request,'Add one open tracking before adding a Training')
          return redirect(self.get_success_url())
      return super().dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.get_success_url()
    return context
  
  def form_valid(self, form):
    form.instance.version = Tracking.get_last_version()
    return super().form_valid(form)
  
  def get_success_url(self):
     d_kwargs = dict( language_id = 1)
     return reverse_lazy('trainings:list', kwargs = d_kwargs)

###############################
#########   L I S T   #########
###############################

def training_list_view(request, language_id):

    request.session['language_id'] = language_id
    url_back = reverse_lazy('languages:list')

    if not Language.objects.exists():
        message = 'You need to add at least one Language'
        messages.error(request, message)
        return redirect(url_back)

    last_version = Tracking.get_last_version()
    l_training_translation = []
    trainings = Training.objects.all()
    for training in trainings:
        query = TrainingTranslation.objects.filter(training_id=training.id, language_id=language_id)
        if query.exists():
            training_translation = query.first()
        else:
            training_translation = TrainingTranslation(training_id=training.id, language_id=language_id, version=last_version)
            training_translation.save()

        l_training_translation.append(training_translation)

    l_training = zip(trainings, l_training_translation)

    context = dict(
        language=Language.objects.get(id=language_id),
        list_training=l_training,
        language_widget=LanguageForm.get_language_widget(language_id),
        url_back=url_back
    )

    return render(request, 'trainings/list.html', context)


###############################
#######   D E T A I L   #######
###############################

def training_detail_view(request, training_id):

    language_id = get_session_language(request)

    training = Training.objects.get(id=training_id)
    context = dict(
        training = training,
        language_id=language_id,
        url_back=reverse_lazy('trainings:list', kwargs=dict(language_id=language_id)),
    )

    return render(request, 'trainings/detail.html', context)

###############################
#######   U P D A T E   #######
###############################

class TrainingUpdateView(UpdateView):
  model = Training
  form_class = TrainingForm
  template_name = 'trainings/update.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.get_success_url()
    context['url_delete'] = reverse_lazy('trainings:delete', kwargs=dict(pk=self.kwargs['pk']))
    return context
  
  def form_valid(self, form):
    form.instance.version = Tracking.get_last_version()
    return super().form_valid(form)
  
  def get_success_url(self) -> str:
     d_kwargs = dict(language_id=get_session_language(self.request))
     return reverse_lazy('trainings:list', kwargs=d_kwargs)

###############################
#######   D E L E T E   #######
###############################

class TrainingDeleteView(DeleteView):
  model = Training
  template_name = 'trainings/delete.html'
  success_url = reverse_lazy('trainings:list')

  def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['url_cancel'] = self.success_url
    return context
  

def get_session_language(request):
   return request.session.get('language_id',1)