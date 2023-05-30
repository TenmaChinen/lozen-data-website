from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
	path('download_exercises_info_json',views.download_exercise_info_json, name='download_exercises_info_json'),
	path('download_exercises_info_json_file',views.download_exercise_info_json_file, name='download_exercises_info_json_file'),
	path('download_exercises_csv/<int:program_id>',views.download_exercises_csv, name='download_exercises_csv'),
	path('download_changes',views.download_changes, name='download_changes'),
]