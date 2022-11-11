"""useful_course_back URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from src.auth import views


urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/', include('src.routers')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.LoginGoogle.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
