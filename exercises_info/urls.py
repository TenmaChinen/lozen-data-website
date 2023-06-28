from django.urls import path
from exercises_info import views

app_name = 'exercises_info'

urlpatterns = [
	path('create',views.ExerciseInfoCreateView.as_view(), name='create'),
	path('list',views.exercise_info_list_view, name='list'),
	path('list?language_id=<int:language_id>/',views.exercise_info_list_view, name='list'),
	path('detail?exercise_info_id=<int:pk>',views.ExerciseInfoDetailView.as_view(), name='detail'),
	path('update?exercise_info_id=<int:pk>',views.ExerciseInfoUpdateView.as_view(), name='update'),
	path('delete?exercise_info_id=<int:pk>',views.ExerciseInfoDeleteView.as_view(), name='delete'),
	path('upload',views.exercise_info_upload_view, name='upload'),
]