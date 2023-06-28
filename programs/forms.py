from programs.models import Program
from django import forms


class FormProgram(forms.ModelForm):
  
  class Meta:
    model = Program
    exclude = ('training', 'version', )


  def disable(self):
    self.fields['unique_id'].widget.attrs['readonly'] = True