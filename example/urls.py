from django.contrib import admin
from django.urls import path, include

from .utils import build_urlpatterns


urlpatterns = [
    path('', include('drive.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += build_urlpatterns()
