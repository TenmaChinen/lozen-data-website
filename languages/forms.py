from languages.models import Language
from django import forms


class LanguageForm(forms.ModelForm):
  
  class Meta:
    model = Language
    fields = ('id','abbreviation',)

  
  # def __init__(self, *args, **kwargs):
      # super().__init__(*args, **kwargs)
      # self.fields['id'].required = False
  

  @classmethod
  def get_language_widget(cls, language_id):
    languages = Language.objects.all()
    
    # l_language = languages.values_list('id', flat=True)
    # l_abbreviation = languages.values_list('abbr', flat=True)
  
    language_widget = LanguageForm().fields['id'].widget
    d_choice = dict(language_widget.choices)

    # import pdb; pdb.set_trace()
    language_widget.value = language_id
    # import pdb; pdb.set_trace()
    # language_widget.choices = [ (k,lang) for k,lang in language_widget.choices if k in l_language ]
    language_widget.choices = languages.values_list('id','abbreviation')
    return language_widget