from programs_translations import views
from django.urls import path

app_name = 'programs_translations'

urlpatterns  = [
	path('update?program_id=<int:program_id>&language_id=<int:language_id>',views.program_translation_update_view, name='update'),
	path('detail?program_id=<int:program_id>&language_id=<int:language_id>',views.program_translation_detail_view, name='detail'),
]