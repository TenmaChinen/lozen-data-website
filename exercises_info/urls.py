from django.urls import path
from exercises_info import views

app_name = 'exercises_info'

urlpatterns = [
	path('create',views.ExerciseInfoCreateView.as_view(), name='create'),
	path('list',views.ExerciseInfoListView.as_view(), name='list'),
	path('detail/<int:pk>',views.ExerciseInfoDetailView.as_view(), name='detail'),
	path('update/<int:pk>',views.ExerciseInfoUpdateView.as_view(), name='update'),
	path('delete/<int:pk>',views.ExerciseInfoDeleteView.as_view(), name='delete'),
	path('upload',views.exercise_info_upload_view, name='upload'),
]