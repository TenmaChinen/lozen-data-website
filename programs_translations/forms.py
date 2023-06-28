from programs_translations.models import ProgramTranslation
from django import forms

class FormProgramTranslation(forms.ModelForm):
  
  class Meta:
    model = ProgramTranslation
    exclude = ('program', 'version', )

  def disable(self):
    self.fields['title'].widget.attrs['disabled'] = True
    self.fields['description'].widget.attrs['disabled'] = True
    self.fields['must_know'].widget.attrs['disabled'] = True
    self.fields['requirements'].widget.attrs['disabled'] = True
