from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
]
