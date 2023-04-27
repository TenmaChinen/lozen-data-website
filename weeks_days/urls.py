from django.urls import path
from weeks_days import views

app_name = 'weeks_days'

urlpatterns = [
	path('list_week/<int:program_id>',views.WeekListView.as_view(), name='list_week'),
	path('create_week/<int:program_id>',views.add_week, name='create_week'),
  
	path('list_day/<int:week_id>',views.DayListView.as_view(), name='list_day'),
	path('create_day/<int:week_id>',views.add_day, name='create_day'),

	# path('update/<int:pk>',views.ExerciseUpdateView.as_view(), name='update'),
	# path('detail/<int:pk>',views.ExerciseDetailView.as_view(), name='detail'),
]