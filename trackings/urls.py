from django.urls import path
from trackings import views

app_name = 'trackings'

urlpatterns = [
  path('create',views.TrackingCreateView.as_view(), name='create'),
	path('list',views.TrackingListView.as_view(), name='list'),
  path('update?version_id=<int:pk>',views.TrackingUpdateView.as_view(), name='update'),
]