from django.urls import path, include
from programs import views

app_name = 'programs'

urlpatterns  = [
	path('list/<int:training_id>',views.ProgramListView.as_view(), name='list'),
	path('create/<int:training_id>',views.ProgramCreateView.as_view(), name='create'),
	path('update/<int:pk>',views.ProgramUpdateView.as_view(), name='update'),
	path('detail/<int:pk>',views.ProgramDetailView.as_view(), name='detail'),
	path('delete/<int:pk>',views.ProgramDeleteView.as_view(), name='delete'),
]