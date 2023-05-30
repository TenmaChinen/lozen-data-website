from django.urls import path, include
from programs import views

app_name = 'programs'

urlpatterns  = [
	path('list?training_id=<int:training_id>&language_id=<int:language_id>',views.program_list_view, name='list'),
	path('create?training_id=<int:training_id>',views.ProgramCreateView.as_view() , name='create'),
	path('update?program_id=<int:pk>',views.ProgramUpdateView.as_view(), name='update'),
	path('detail?program_id=<int:pk>',views.ProgramDetailView.as_view(), name='detail'),
	path('delete?program_id=<int:pk>',views.ProgramDeleteView.as_view(), name='delete'),
]