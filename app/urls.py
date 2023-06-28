from django.views.generic import RedirectView
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='trainings/list')),
    
    path('trainings/', include('trainings.urls')),
    path('trainings_translations/', include('trainings_translations.urls')),
    
    path('programs/', include('programs.urls')),
    path('programs_translations/', include('programs_translations.urls')),
    
    path('exercises_info/', include('exercises_info.urls')),
    path('exercises_info_translations/', include('exercises_info_translations.urls')),
    
    path('exercises/', include('exercises.urls')),
    path('trackings/', include('trackings.urls')),
    path('languages/', include('languages.urls')),

    path('api/', include('api.urls')),
]
