from exercises.models import Exercise
from django import forms


class ExerciseForm(forms.ModelForm):

    rest_minutes = forms.IntegerField(min_value=0, initial=0)
    rest_seconds = forms.IntegerField(min_value=0, max_value=59, initial=0)

    class Meta:
        model = Exercise
        exclude = ('program', 'idx', 'rest', 'version',)

    def clean(self):
        cleaned_data = super().clean()
        minutes = cleaned_data.get('rest_minutes')
        seconds = cleaned_data.get('rest_seconds')
        rest_time = minutes * 60 + seconds
        cleaned_data['rest'] = rest_time
        return cleaned_data

    def disable(self):
        self.fields['exercise_info'].widget.attrs['disabled'] = True
        self.fields['week'].widget.attrs['disabled'] = True
        self.fields['day'].widget.attrs['disabled'] = True
        self.fields['sets'].widget.attrs['disabled'] = True
        self.fields['unit_value'].widget.attrs['disabled'] = True
        self.fields['percent'].widget.attrs['disabled'] = True
        self.fields['power'].widget.attrs['disabled'] = True
        self.fields['rir'].widget.attrs['disabled'] = True
        self.fields['rest_minutes'].widget.attrs['disabled'] = True
        self.fields['rest_seconds'].widget.attrs['disabled'] = True
        # self.fields['rest'].widget.attrs['disabled'] = True