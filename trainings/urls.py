from django.urls import path, include
from trainings import views

app_name = 'trainings'

urlpatterns = [
	path('list/',views.TrainingListView.as_view(), name='list'),
	path('create/',views.TrainingCreateView.as_view(), name='create'),
	path('update/<int:pk>',views.TrainingUpdateView.as_view(), name='update'),
	path('delete/<int:pk>',views.TrainingDeleteView.as_view(), name='delete'),
]