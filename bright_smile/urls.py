"""
URL configuration for bright_smile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views
from django.conf.urls import handler404
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve
from django.contrib.auth.decorators import login_required
from .views import get_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(lambda request: redirect('clinics/')), name='home'),
    path('clinics/', include('clinics.urls'),name='clinics'),  
    path('doctors/', include('doctors.urls'),name='doctors'),  
    path('patients/', include('patients.urls'),name='patients'),  
    path('procedures/', include('procedures.urls'),name='procedures'),  
    # path('schedules/', include('schedules.urls'),name='schedules'),  
    path('appointments/', include('appointments.urls')),
    path('', include('members.urls')),
    path('api/get-token/', get_auth_token, name='get_auth_token'),
    
]
# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # else:
    # This is key for serving static files with DEBUG=False
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
handler404 = TemplateView.as_view(template_name='404.html')