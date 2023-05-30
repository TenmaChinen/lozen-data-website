from programs_translations.models import ProgramTranslation
from django import forms

class FormProgramTranslation(forms.ModelForm):
  
  class Meta:
    model = ProgramTranslation
    exclude = ('program', 'version', )
