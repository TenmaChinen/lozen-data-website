from programs.models import Program, ProgramTranslation
from django import forms


class FormProgram(forms.ModelForm):
  
  class Meta:
    model = Program
    exclude = ('training', )


class FormProgramTranslation(forms.ModelForm):
  
  class Meta:
    model = ProgramTranslation
    exclude = ('program', )
