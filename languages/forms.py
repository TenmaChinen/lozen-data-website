from languages.models import Language
from django import forms


class LanguageForm(forms.ModelForm):
  
  class Meta:
    model = Language
    fields = ('id',)


  @classmethod
  def get_language_widget(cls, language_id):
    l_language = Language.objects.all().values_list('id', flat=True)
    language_widget = LanguageForm().fields['id'].widget
    language_widget.value = language_id
    language_widget.choices = [ (k,v) for k,v in language_widget.choices if k in l_language ]
    return language_widget