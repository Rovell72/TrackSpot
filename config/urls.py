"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
import re

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings

from core.views import media_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('tracks/', include('tracks.urls')),
]

# Файлы (аватарки, обложки, аудио) отдаются из базы данных, а не из папки media/
urlpatterns += [
    re_path(r'^%s(?P<name>.+)$' % re.escape(settings.MEDIA_URL.lstrip('/')), media_file, name='media_file'),
]
