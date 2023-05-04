from django.urls import path, include
from languages import views

app_name = 'languages'

urlpatterns = [
	path('list/',views.LanguageListView.as_view(), name='list'),
	path('create/',views.LanguageCreateView.as_view(), name='create'),
	path('update/<int:pk>',views.LanguageUpdateView.as_view(), name='update'),
	path('delete/<int:pk>',views.LanguageDeleteView.as_view(), name='delete'),
]