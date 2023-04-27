from programs.models import Program
from django import forms


class ProgramForm(forms.ModelForm):
  
  class Meta:
    model = Program
    exclude = ('training', )
