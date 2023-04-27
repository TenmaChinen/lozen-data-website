from trainings.models import Training
from django import forms


class TrainingForm(forms.ModelForm):
  
  class Meta:
    model = Training
    fields = '__all__'