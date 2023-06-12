from trainings_translations import views
from django.urls import path, include

app_name = 'trainings_translations'

urlpatterns = [
	path('detail?training_id=<int:training_id>&language_id=<int:language_id>',views.training_translation_detail_view, name='detail'),
	path('update?training_id=<int:training_id>&language_id=<int:language_id>',views.training_translation_update_view, name='update'),
]