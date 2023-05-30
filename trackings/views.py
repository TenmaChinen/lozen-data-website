from typing import Any, Dict, Optional, Type
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy
# from django.shortcuts import render
from django.utils import timezone

from trackings.forms import FormCreateTracking, FormUpdateTracking
from trackings.models import Tracking

###############################
#######   C R E A T E   #######
###############################

class TrackingCreateView(CreateView):
    form_class = FormCreateTracking
    template_name = 'trackings/create.html'
    success_url = reverse_lazy('trackings:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_cancel'] = self.success_url
        return context
    
    def get_form(self, form_class=None):
        if Tracking.objects.exists():
            next_version = Tracking.objects.latest('version').version + 1
        else:
            next_version = 1
        form = super().get_form(form_class)
        form.fields['version'].initial = next_version
        return form

###############################
#########   L I S T   #########
###############################

class TrackingListView(ListView):
    model = Tracking
    template_name = 'trackings/list.html'
    context_object_name = 'list_tracking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            is_add_disabled = not Tracking.is_add_track_allowed(),
            current_version = Tracking.get_last_version()
        ))
        return context

###############################
#######   U P D A T E   #######
###############################

class TrackingUpdateView(UpdateView):
    model = Tracking
    form_class = FormUpdateTracking
    template_name = 'trackings/update.html'
    context_object_name = 'tracking'

    def get_success_url(self):
        return reverse_lazy('trackings:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_back'] = self.get_success_url()
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['state_aux'].initial = Tracking.state.field.choices[0][1]
        return form

    def form_valid(self, form):
        form.instance.version = self.kwargs['pk']
        form.instance.state = True
        form.instance.release_date = timezone.now().date()
        return super().form_valid(form)