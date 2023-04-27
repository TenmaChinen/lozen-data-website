from django.urls import path
from exercises import views

app_name = 'exercises'

urlpatterns = [
	path('list/<int:day_id>',views.ExerciseListView.as_view(), name='list'),
	path('create/<int:day_id>',views.ExerciseCreateView.as_view(), name='create'),
	# path('update/<int:pk>',views.ExerciseUpdateView.as_view(), name='update'),
	# path('detail/<int:pk>',views.ExerciseDetailView.as_view(), name='detail'),
]