"""hqjy_ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import xadmin
from . import views

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', views.index, name='index'),
    path('system_maintenance/', views.check_system_open_or_close, name='check_system_open_or_close'),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('mainsite/', include('ems_mainsite.urls')),
    path('ems-account/', include('ems_account.urls')),
    path('search/', include('haystack.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
