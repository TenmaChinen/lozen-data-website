from django.views.generic import RedirectView
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='trainings/list/')),
    path('trainings/', include('trainings.urls')),
    path('programs/', include('programs.urls')),
    path('exercises/', include('exercises.urls')),
    path('weeks_days/', include('weeks_days.urls')),
]
