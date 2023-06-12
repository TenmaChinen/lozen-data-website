from django.http import HttpResponse, JsonResponse
from django.middleware import csrf
from pandas import DataFrame, merge
import json

from languages.models import Language

from exercises_info.models import ExerciseInfo
from exercises_info_translations.models import ExerciseInfoTranslation

from exercises.models import Exercise
from trackings.models import Tracking
from trainings.models import Training
from trainings_translations.models import TrainingTranslation

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
        from exercises_info.views import get_exercises_info_dict
        d_exercises_info = get_exercises_info_dict()

        response = HttpResponse(content_type='application/json')
        file_name = f'exercises_info.json'
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        json.dump(obj=d_exercises_info, fp=response, indent=2, ensure_ascii=False)

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
    
   ###################
   ####   G E T   ####
   ###################

    if request.method == 'GET':
        csrf_token = csrf.get_token(request)
        response = JsonResponse( {'message':'Success'})
        response['X-CSRFToken'] = csrf_token
        return response

    ###################
    ###   P O S T   ###
    ###################

    elif request.method == 'POST':
        d_data = json.loads(request.body.decode('utf-8'))

        web_version = Tracking.get_last_version_released()
        app_version = d_data.get('version')
        app_language = d_data.get('language')
        d_return = {}
            
        if None not in [web_version, app_version, app_language] and ( app_version != web_version ):
            
            l_version = list(range(app_version+1, web_version+1))

           #######################################
           #########   L A N G U A G E   #########
           #######################################

            queryset = Language.objects.filter(abbreviation = app_language)
            if queryset.exists():
                language_id = queryset.first().id
            else:
                language_id = Language.objects.filter(abbreviation = 'en').id
            
            #######################################
            ####   E X E R C I S E   I N F O   ####
            #######################################
            
            df_1, df_2 = None, None

            queryset = ExerciseInfo.objects.filter(version__in = l_version)
            if queryset.exists():
                df_1 = DataFrame.from_records(data=queryset.values('id'))

            queryset = ExerciseInfoTranslation.objects.filter(version__in = l_version, language_id=language_id)
            if queryset.exists():
                df_2 = DataFrame.from_records(data=queryset.values('exercise_info_id', 'title', 'description'))

            df_3 = merge_data_frames(df_1, df_2, left_on='id', right_on='exercise_info_id')
            
            if df_3:
                d_return['exercises_info'] = df_3

            #######################################
            #########   T R A I N I N G   #########
            #######################################

            df_1, df_2 = None, None

            queryset = Training.objects.filter(version__in = l_version)
            if queryset.exists():
                df_1 = DataFrame.from_records(data=queryset.values('id'))
            
            queryset = TrainingTranslation.objects.filter(version__in = l_version, language_id=language_id)
            if queryset.exists():
                df_2 = DataFrame.from_records(data=queryset.values('training_id', 'title'))
            
            df_3 = merge_data_frames(df_1,df_2, left_on='id', right_on='training_id')
            if df_3:
                d_return['trainings'] = df_3

            #######################################
            #########   P R O G R A M S   #########
            #######################################

            df_1, df_2 = None, None
            
            queryset = Program.objects.filter(version__in = l_version)
            if queryset.exists():
                df_1 = DataFrame.from_records(data=queryset.values('id', 'training_id'))

            queryset = ProgramTranslation.objects.filter(version__in = l_version, language_id=language_id)
            if queryset.exists():
                values = queryset.values('program_id', 'title', 'description', 'must_know', 'requirements')
                df_2 = DataFrame.from_records(data=values)
            
            df_3 = merge_data_frames(df_1, df_2, left_on='id', right_on='program_id')
            if df_3:
                d_return['programs'] = df_3

            #######################################
            ########   E X E R C I S E S   ########
            #######################################

            queryset = Exercise.objects.filter(version__in = l_version)
            if queryset.exists():
                values = queryset.values('exercise_info_id', 'program_id', 'week', 'day', 'idx', 'sets', 'reps', 'percent', 'power', 'rir', 'rest' )
                df = DataFrame.from_records(data=values)
                d_return['exercises'] = df.to_dict(orient='list')
            
            d_return['version'] = web_version
            return JsonResponse(d_return)

        # status= 204 is No Content Response
        return JsonResponse(data=d_return, status=204)
    

###############################
########   U T I L S   ########
###############################

def merge_data_frames(df_1, df_2, left_on, right_on):
    if df_1 is not None and df_2 is not None:
        df_3 = merge(left=df_1, right=df_2, left_on=left_on, right_on=right_on, how='outer')
        df_3[left_on] = df_3[left_on].combine_first(df_3[right_on])
        df_3.drop(right_on, axis=1, inplace=True)
        df_3[left_on] = df_3[left_on].astype(int)
        df_3.replace(float('Nan'),None, inplace=True)

    elif df_1 is not None:
        df_1.rename(columns={left_on : 'id'}, inplace=True)
        df_3 = df_1
    elif df_2 is not None:
        df_2.rename(columns={right_on : 'id'}, inplace=True)
        df_3 = df_2
    else:
        return None
    

    return df_3.to_dict(orient='list')