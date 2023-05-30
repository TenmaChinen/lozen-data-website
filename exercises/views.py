from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from io import StringIO
import pandas as pd

from exercises.forms import ExerciseForm
from exercises.models import Exercise
from trackings.models import Tracking
from programs.models import Program


###############################
#######   C R E A T E   #######
###############################

class ExerciseCreateView(CreateView):
    form_class = ExerciseForm
    template_name = 'exercises/create.html'

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
          return redirect(self.success_url)
      return super().dispatch(request, *args, **kwargs)

    # TODO : Document the "get_initial" override to initialize forms
    def get_initial(self):
        initial = super().get_initial()
        initial['week'] = self.kwargs['week']
        initial['day'] = self.kwargs['day']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)  # week & day
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.program_id = self.kwargs['program_id']
        week, day = self.kwargs['week'], self.kwargs['day']
        exercises = Exercise.objects.filter(week=week, day=day)
        if exercises.exists():
            new_index = exercises.latest('idx').idx + 1
        else:
            new_index = 1

        form.instance.idx = new_index
        form.instance.rest = form.cleaned_data['rest']
        form.instance.version = Tracking.get_last_version()

        return super().form_valid(form)

    def get_success_url(self):
        # TODO : Document that we can get the data defined in form is available here as "self.object"
        d_kwargs = {
            'program_id': self.kwargs['program_id'],
            'week': self.object.week,
            'day': self.object.day
        }
        return reverse_lazy('exercises:list', kwargs=d_kwargs)


###############################
#########   L I S T   #########
###############################

class ExerciseListView(ListView):
    model = Exercise
    template_name = 'exercises/list.html'
    context_object_name = 'list_exercise'

    # TODO : Document "get_queryset" override to filter ListView
    def get_queryset(self):
        queryset = super().get_queryset()
        program_id = self.kwargs['program_id']
        week = self.kwargs['week']
        day = self.kwargs['day']
        return queryset.filter(program_id=program_id, week=week, day=day)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)

        # TODO : Document how to get Form widgets or raw field
        exercise_form_fields = ExerciseForm().fields
        week_widget = exercise_form_fields['week'].widget
        day_widget = exercise_form_fields['day'].widget

        # Forced attribute to track selected option ( invented attribute )
        week_widget.value = self.kwargs['week']
        day_widget.value = self.kwargs['day']

        program_id = self.kwargs['program_id']
        url_back = reverse_lazy('programs_translations:detail', kwargs=dict(language_id=1, program_id=program_id))
        program_unique_id = Program.objects.get(id=program_id).unique_id
        context.update(dict(
            current_version = Tracking.get_last_version(),
            program_unique_id=program_unique_id,
            week_widget=week_widget,
            day_widget=day_widget,
            url_back=url_back))

        return context

###############################
#######   U P D A T E   #######
###############################

class ExerciseUpdateView(UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'exercises/update.html'

    def dispatch(self, request, *args, **kwargs):
      if Tracking.is_last_version_released():
            exercise = Exercise.objects.get(pk=self.kwargs['pk'])
            d_kwargs = dict(program_id=exercise.program.id, week=exercise.week, day=exercise.day)
            url_back = reverse_lazy('exercises:list', kwargs=d_kwargs)
            return redirect(url_back)
      return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        week, day = self.object.week, self.object.day
        d_kwargs = dict(program_id=self.object.program.id, week=week, day=day)
        return reverse_lazy('exercises:list', kwargs=d_kwargs)

    # TODO : Document how to set values in form ( using get_initial )
    # def get_initial(self):
    #   initial = super().get_initial()
    #   rest_total_seconds = self.object.rest
    #   initial['rest_minutes'] = rest_total_seconds // 60
    #   initial['rest_seconds'] = rest_total_seconds % 60
    #   return initial

    # TODO : Document how to set values in form ( using get_form )
    def get_form(self):
        form = super().get_form(ExerciseForm)
        rest_total_seconds = form.instance.rest
        # rest_total_seconds = self.object.rest # This works as well
        form.fields['rest_minutes'].initial = rest_total_seconds // 60
        form.fields['rest_seconds'].initial = rest_total_seconds % 60

        return form

    # TODO : Document how to reasign exlucded form fields.
    def form_valid(self, form):
        form.instance.rest = form.cleaned_data['rest']
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program_id, week, day = self.object.program_id, self.object.week, self.object.day
        context.update(
            url_back=reverse_lazy('exercises:list', kwargs=dict(program_id=program_id, week=week, day=day)),
            url_delete=reverse_lazy('exercises:delete', kwargs=dict(pk=self.object.id))
        )
        return context
    

###############################
#######   D E L E T E   #######
###############################

class ExerciseDeleteView(DeleteView):
    model = Exercise
    template_name = 'exercises/delete.html'

    def get_success_url(self):
        d_kwargs = dict(
            program_id=self.object.program_id,
            week=self.object.week,
            day=self.object.day,
        )

        return reverse_lazy('exercises:list', kwargs=d_kwargs)

###############################
#######   U P L O A D   #######
###############################

def exercise_upload_view(request, program_id):

    program = Program.objects.get(id=program_id)
    
    ###################
    ####   G E T   ####
    ###################
    if request.method == 'GET':
        list_exercise = Exercise.objects.filter(program_id=program_id)
        list_exercise = list_exercise.order_by('week', 'day', 'idx')

        l_field_name = Exercise.get_csv_fields()
        exercise_values = list_exercise.values(*l_field_name)

        # TODO : Document the "DataFrame.from_records"
        df_exercises = pd.DataFrame.from_records(
            data=exercise_values, columns=l_field_name)

        csv_exercises = df_exercises.to_csv(index=False)

        context = {'program': program, 'raw_csv': csv_exercises}

        return render(request, 'exercises/upload.html', context)

    ###################
    ###   P O S T   ###
    ###################
    else:

        raw_csv = request.POST['raw_csv']
        raw_csv_io = StringIO(raw_csv)
        df_exercises = pd.read_csv(raw_csv_io)
        df_exercises.sort_values(by=['week', 'day', 'idx'], inplace=True)

        queryset = Exercise.objects.filter(program_id=program_id)
        l_pack = [ [int(w), int(d), int(i)] for w,d,i in queryset.values_list('week','day','idx') ]
        index_filter = df_exercises.apply( lambda row : [row.week, row.day, row['idx']] in l_pack, axis=1 )
        df_exercises_old = df_exercises[index_filter]
        df_exercises_new = df_exercises[-index_filter]

        # Update old rows
        last_version = Tracking.get_last_version()    
    
        for _, row in df_exercises_old.iterrows():
            d_row = row[['week','day','idx']].to_dict()
            instance = Exercise.objects.get(program_id=program_id, **d_row)
            for key, value in row.drop(['week','day','idx']).to_dict().items():
                setattr(instance, key, value )
            instance.version = last_version
            instance.save()

        # Save New Rows
        l_instances = []
        for _, row in df_exercises_new.iterrows():
            d_row = row.to_dict()

            instance = Exercise(program_id=program_id, **d_row)
            instance.version = last_version
            l_instances.append(instance)
        
        Exercise.objects.bulk_create(l_instances)
        

        # TODO : Document the "Model.objects.bulk_create"
        # ( fast way to create multiple instances without using save() per each instance )

        return redirect('exercises:list', program_id=program_id, week=1, day=1)