from django.http import HttpResponse, JsonResponse
from django.middleware import csrf
from pandas import DataFrame
import json

from languages.models import Language
from exercises_info.models import ExerciseInfo
from exercises.models import Exercise
from trackings.models import Tracking
from trainings.models import Training
from programs.models import Program
from programs_translations.models import ProgramTranslation
from exercises.models import Exercise

def download_exercise_info_json(request):
    if request.method == 'GET':
        exercises_info = ExerciseInfo.objects.all()

        exercises_info_values = exercises_info.values()
        df_exercises_info = DataFrame(data=exercises_info_values)
        d_exercises_info = df_exercises_info.to_dict()

        return JsonResponse(d_exercises_info)


def download_exercise_info_json_file(request):
    if request.method == 'GET':
        exercises_info = ExerciseInfo.objects.all()

        exercises_info_values = exercises_info.values()
        df_exercises_info = DataFrame(data=exercises_info_values)
        d_exercises_info = df_exercises_info.to_dict()

        response = HttpResponse(content_type='application/json')
        file_name = f'exercises_info.json'
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        json.dump(obj=d_exercises_info, fp=response, indent=2)

        return response

def download_exercises_csv(request, program_id):
    if request.method == 'GET':
        response = HttpResponse(content_type='text/csv')
        file_name = f'program_exercises_id_{program_id}.csv'
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        exercises = Exercise.objects.filter(program_id=program_id)

        l_field_name = Exercise.get_csv_fields()
        exercises_values = exercises.values(*l_field_name)

        df_exercises = DataFrame.from_records(data=exercises_values, columns=l_field_name)
        raw_csv = df_exercises.to_csv(index=False)
        response.write(raw_csv)

        return response



def download_changes(request):
    if request.method == 'GET':
        csrf_token = csrf.get_token(request)
        response = JsonResponse( {'message':'Success'})
        response['X-CSRFToken'] = csrf_token
        return response
    
    elif request.method == 'POST':
        d_data = json.loads(request.body.decode('utf-8'))

        app_version = d_data['version']
        web_version = Tracking.get_last_version_released()
        
        if (web_version is not None) and ( app_version != web_version ):
            l_version = list(range(app_version+1, web_version+1))

            d_return = {}

            # Languages
            queryset = Language.objects.filter(version__in = l_version)
            if queryset.exists():
                l_languages = [ x for x in queryset.values('id') ]
                d_id_to_language = dict(Language.LANGUAGE_CHOICES)
                for d_language in l_languages:
                    d_language['title'] = d_id_to_language[d_language['id']]

                df = DataFrame.from_records(data=l_languages)
                
                d_return['languages'] = df.to_dict(orient='list')
            
            # Exercise Info
            queryset = ExerciseInfo.objects.filter(version__in = l_version)
            if queryset.exists():
                values = queryset.values('id', 'title', 'description')
                df = DataFrame.from_records(data=values)
                d_return['exercises_info'] = df.to_dict(orient='list')

            # Trainings
            queryset = Training.objects.filter(version__in = l_version)
            if queryset.exists():
                values = queryset.values('id', 'title')
                df = DataFrame.from_records(data=values)
                d_return['trainings'] = df.to_dict(orient='list')

            # Programs
            queryset = Program.objects.filter(version__in = l_version)
            if queryset.exists():
                values = queryset.values('unique_id', 'training_id')
                df = DataFrame.from_records(data=values)
                d_return['programs'] = df.to_dict(orient='list')

            # Programs Translations
            queryset = ProgramTranslation.objects.filter(version__in = l_version)
            if queryset.exists():
                values = queryset.values('program_id', 'language_id', 'title', 'description', 'must_know', 'requirements' )
                df = DataFrame.from_records(data=values)
                d_return['programs_translations'] = df.to_dict(orient='list')

            # Exercises
            queryset = Exercise.objects.filter(version__in = l_version)
            if queryset.exists():
                values = queryset.values('exercise_info_id', 'program_id', 'week', 'day', 'idx', 'sets', 'reps', 'percent', 'power', 'rir', 'rest' )
                df = DataFrame.from_records(data=values)
                d_return['exercises'] = df.to_dict(orient='list')
            
            d_return['version'] = web_version
            return JsonResponse(d_return)

        # status= 204 is No Content Response
        return JsonResponse(data={}, status=204)