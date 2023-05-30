from trackings.models import Tracking
from django import forms


class FormCreateTracking(forms.ModelForm):
  
  class Meta:
    model = Tracking
    fields = ('version', )
  
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['version'].widget.attrs['readonly'] = True

class FormUpdateTracking(forms.ModelForm):
  
  state_aux = forms.CharField(widget=forms.TextInput(attrs=dict(readonly=True)), label='State')

  class Meta:
    model = Tracking
    fields = ('version', 'state_aux', 'release_date')

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['version'].widget.attrs['readonly'] = True
      self.fields['release_date'].widget.attrs['readonly'] = True
