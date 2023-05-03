from django.urls import path
from exercises import views

app_name = 'exercises'

# TODO : Document this kind of pattern "%3Fvar1=<>&var2=<>&var3=<>" where "%3F" = "?" Question Mark

urlpatterns = [
	path(r'list?program_id=<int:program_id>&week=<int:week>&day=<int:day>',views.ExerciseListView.as_view(), name='list'),
	path('create?program_id=<int:program_id>&week=<int:week>&day=<int:day>',views.ExerciseCreateView.as_view(), name='create'),
	path('update/<int:pk>',views.ExerciseUpdateView.as_view(), name='update'),
	path('upload/<int:program_id>',views.exercise_upload_view, name='upload'),
	path('download/<int:program_id>',views.exercise_download, name='download'),
	path('delete/<int:pk>',views.ExerciseDeleteView.as_view(), name='delete'),
]