from django.urls import path, include
from programs import views

app_name = 'programs'

urlpatterns  = [
	path('list?training_id=<int:training_id>&language_id=<int:language_id>',views.program_list_view, name='list'),
	path('create?training_id=<int:training_id>&language_id=<int:language_id>',views.program_create_view , name='create'),
	path('update?program_id=<int:program_id>&language_id=<int:language_id>',views.program_update_view, name='update'),
	path('detail?program_id=<int:program_id>&language_id=<int:language_id>',views.program_detail_view, name='detail'),
	path('delete?program_id=<int:program_id>&language_id=<int:language_id>',views.ProgramDeleteView.as_view(), name='delete'),
]