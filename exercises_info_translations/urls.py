from exercises_info_translations import views
from django.urls import path

app_name = 'exercises_info_translations'

urlpatterns = [
	path('update?exercise_info_id=<int:exercise_info_id>&language_id=<int:language_id>',views.exercise_info_translation_update_view, name='update'),
	path('detail?exercise_info_id=<int:exercise_info_id>&language_id=<int:language_id>',views.exercise_info_translation_detail_view, name='detail'),
]